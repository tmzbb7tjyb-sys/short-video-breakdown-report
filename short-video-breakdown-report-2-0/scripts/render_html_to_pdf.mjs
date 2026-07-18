#!/usr/bin/env node
import { spawn } from "node:child_process";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

function arg(name, fallback) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

const input = process.argv[2];
const output = process.argv[3];
if (!input || !output) {
  console.error("Usage: node render_html_to_pdf.mjs <input.html> <output.pdf> [--width 1080] [--chrome /path/to/chrome]");
  process.exit(2);
}

const width = Number(arg("--width", "1080"));
const chromePath = arg("--chrome", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome");
const port = Number(arg("--port", String(9800 + Math.floor(Math.random() * 500))));
const pxPerInch = 96;

function delay(ms) {
  return new Promise((resolveDelay) => setTimeout(resolveDelay, ms));
}

async function waitForJson(url, tries = 100) {
  let lastError;
  for (let i = 0; i < tries; i += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
      lastError = new Error(`HTTP ${response.status}`);
    } catch (error) {
      lastError = error;
    }
    await delay(100);
  }
  throw lastError ?? new Error(`Timed out waiting for ${url}`);
}

function client(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let nextId = 1;
  const pending = new Map();
  const listeners = new Map();

  ws.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    if (message.id && pending.has(message.id)) {
      const { resolve: resolvePending, reject } = pending.get(message.id);
      pending.delete(message.id);
      message.error ? reject(new Error(JSON.stringify(message.error))) : resolvePending(message.result);
      return;
    }
    const callbacks = listeners.get(message.method);
    if (callbacks) callbacks.forEach((callback) => callback(message));
  });

  const ready = new Promise((resolveReady, reject) => {
    ws.addEventListener("open", resolveReady, { once: true });
    ws.addEventListener("error", reject, { once: true });
  });

  async function send(method, params = {}, sessionId) {
    await ready;
    const id = nextId++;
    const payload = { id, method, params };
    if (sessionId) payload.sessionId = sessionId;
    const result = new Promise((resolveSend, reject) => pending.set(id, { resolve: resolveSend, reject }));
    ws.send(JSON.stringify(payload));
    return result;
  }

  function on(method, callback) {
    const callbacks = listeners.get(method) ?? [];
    callbacks.push(callback);
    listeners.set(method, callbacks);
  }

  return { send, on, ready, close: () => ws.close() };
}

async function main() {
  const userDataDir = await mkdtemp(join(tmpdir(), "codex-html-pdf-render-"));
  const chrome = spawn(chromePath, [
    "--headless=new",
    "--disable-gpu",
    "--disable-background-networking",
    "--disable-component-update",
    "--disable-sync",
    "--metrics-recording-only",
    "--no-first-run",
    "--no-default-browser-check",
    "--allow-file-access-from-files",
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${userDataDir}`,
  ], { stdio: ["ignore", "ignore", "ignore"] });

  try {
    const version = await waitForJson(`http://127.0.0.1:${port}/json/version`);
    const browser = client(version.webSocketDebuggerUrl);
    await browser.ready;
    const { targetId } = await browser.send("Target.createTarget", { url: "about:blank" });
    const { sessionId } = await browser.send("Target.attachToTarget", { targetId, flatten: true });

    await browser.send("Page.enable", {}, sessionId);
    await browser.send("Runtime.enable", {}, sessionId);
    await browser.send("Emulation.setDeviceMetricsOverride", {
      width, height: 1600, deviceScaleFactor: 1, mobile: false,
    }, sessionId);

    const loaded = new Promise((resolveLoaded) => {
      browser.on("Page.loadEventFired", (message) => {
        if (message.sessionId === sessionId) resolveLoaded();
      });
    });
    await browser.send("Page.navigate", { url: pathToFileURL(resolve(input)).href }, sessionId);
    await loaded;
    await browser.send("Runtime.evaluate", {
      awaitPromise: true,
      expression: "Promise.all(Array.from(document.images).map(img => img.complete ? true : new Promise(r => { img.onload = r; img.onerror = r; })))",
    }, sessionId);

    const metrics = await browser.send("Runtime.evaluate", {
      returnByValue: true,
      expression: `
        (() => {
          const page = document.querySelector('.page') || document.body;
          const originalWidth = page.getBoundingClientRect().width || page.scrollWidth || ${width};
          const scale = ${width} / originalWidth;
          document.documentElement.style.margin = '0';
          document.body.style.margin = '0';
          document.body.style.background = '#fff';
          document.body.style.overflow = 'hidden';
          page.style.margin = '0';
          page.style.boxShadow = 'none';
          page.style.transform = 'none';
          page.style.zoom = String(scale);
          const rect = page.getBoundingClientRect();
          const height = Math.ceil(rect.height) + 4;
          let style = document.getElementById('codex-long-pdf-page-style');
          if (!style) {
            style = document.createElement('style');
            style.id = 'codex-long-pdf-page-style';
            document.head.appendChild(style);
          }
          style.textContent = '@page { size: ${width / pxPerInch}in ' + (height / ${pxPerInch}) + 'in; margin: 0; } * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }';
          return { height, scale };
        })()
      `,
    }, sessionId);

    const height = Math.max(1, Math.ceil(metrics.result.value.height));
    await browser.send("Emulation.setDeviceMetricsOverride", {
      width, height: Math.min(height, 16000), deviceScaleFactor: 1, mobile: false,
    }, sessionId);
    await delay(250);

    const pdf = await browser.send("Page.printToPDF", {
      printBackground: true,
      preferCSSPageSize: false,
      paperWidth: width / pxPerInch,
      paperHeight: height / pxPerInch,
      marginTop: 0,
      marginBottom: 0,
      marginLeft: 0,
      marginRight: 0,
      scale: 1,
    }, sessionId);
    await writeFile(output, Buffer.from(pdf.data, "base64"));
    console.log(`${output} width=${width} height=${height} scale=${metrics.result.value.scale.toFixed(4)} pages=1`);
    browser.close();
  } finally {
    chrome.kill("SIGTERM");
    await delay(300);
    await rm(userDataDir, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
