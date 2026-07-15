import Foundation
import Vision
import AppKit

let args = CommandLine.arguments
guard args.count >= 3 else {
    FileHandle.standardError.write(Data("Usage: swift ocr_subtitles.swift <frames_dir> <out_json>\n".utf8))
    exit(2)
}

let framesDir = URL(fileURLWithPath: args[1], isDirectory: true)
let outURL = URL(fileURLWithPath: args[2])
let files = (try FileManager.default.contentsOfDirectory(at: framesDir, includingPropertiesForKeys: nil))
    .filter { $0.pathExtension.lowercased() == "png" || $0.pathExtension.lowercased() == "jpg" || $0.pathExtension.lowercased() == "jpeg" }
    .sorted { $0.lastPathComponent < $1.lastPathComponent }

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["zh-Hans", "zh-Hant", "en-US"]
request.usesLanguageCorrection = true

var rows: [[String: Any]] = []

for file in files {
    guard let image = NSImage(contentsOf: file),
          let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        continue
    }

    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    do {
        try handler.perform([request])
        let observations = request.results ?? []
        var texts: [String] = []
        for obs in observations {
            guard let top = obs.topCandidates(1).first else { continue }
            let box = obs.boundingBox
            // Keep subtitles and common product-label bands. Vision's origin is bottom-left.
            if box.minY < 0.68 && top.confidence > 0.25 {
                let text = top.string.trimmingCharacters(in: .whitespacesAndNewlines)
                if !text.isEmpty { texts.append(text) }
            }
        }
        let name = file.lastPathComponent
        let parts = name.split(separator: "_")
        let second = parts.count > 1 ? (Double(parts[1]) ?? 0) / 100.0 : 0
        rows.append(["file": name, "second": second, "texts": texts])
        print("\(String(format: "%.2f", second)): \(texts.joined(separator: " | "))")
    } catch {
        FileHandle.standardError.write(Data("OCR failed for \(file.lastPathComponent): \(error)\n".utf8))
    }
}

let data = try JSONSerialization.data(withJSONObject: rows, options: [.prettyPrinted, .sortedKeys])
try data.write(to: outURL)
