import Foundation
import AVFoundation
import AppKit

let args = CommandLine.arguments
guard args.count >= 4 else {
    FileHandle.standardError.write(Data("Usage: swift extract_frames.swift <video> <out_dir> <seconds_csv>\n".utf8))
    exit(2)
}

let videoURL = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2], isDirectory: true)
let seconds = args[3]
    .split(separator: ",")
    .compactMap { Double($0.trimmingCharacters(in: .whitespacesAndNewlines)) }

try FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)

let asset = AVURLAsset(url: videoURL)
let generator = AVAssetImageGenerator(asset: asset)
generator.appliesPreferredTrackTransform = true
generator.requestedTimeToleranceBefore = CMTime(seconds: 0.05, preferredTimescale: 600)
generator.requestedTimeToleranceAfter = CMTime(seconds: 0.05, preferredTimescale: 600)

for second in seconds {
    let requested = CMTime(seconds: second, preferredTimescale: 600)
    do {
        var actual = CMTime.zero
        let cgImage = try generator.copyCGImage(at: requested, actualTime: &actual)
        let rep = NSBitmapImageRep(cgImage: cgImage)
        guard let data = rep.representation(using: .png, properties: [:]) else {
            FileHandle.standardError.write(Data("Failed to encode frame at \(second)\n".utf8))
            continue
        }
        let centiseconds = Int((CMTimeGetSeconds(actual) * 100).rounded())
        let filename = String(format: "frame_%05d_%05d.png", Int(second * 100), centiseconds)
        try data.write(to: outDir.appendingPathComponent(filename))
        print("\(String(format: "%.2f", second)) -> \(filename)")
    } catch {
        FileHandle.standardError.write(Data("Failed at \(second): \(error)\n".utf8))
    }
}
