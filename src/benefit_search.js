import { spawn } from "child_process";
import path from "path";

export async function benefitSearch(text) {
  return new Promise((resolve) => {
    const pyPath = path.resolve("src/benefit_search.py");

    const proc = spawn("python3", [pyPath, text]);

    let output = "";
    let errorOutput = "";

    proc.stdout.on("data", (data) => {
      output += data.toString();
    });

    proc.stderr.on("data", (data) => {
      errorOutput += data.toString();
    });

    proc.on("close", () => {
      if (errorOutput) {
        return resolve({
          ok: false,
          error: errorOutput
        });
      }

      try {
        const json = JSON.parse(output);
        return resolve(json);
      } catch (e) {
        return resolve({
          ok: false,
          error: "Invalid JSON from Python",
          raw: output
        });
      }
    });
  });
}