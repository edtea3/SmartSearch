import { spawn } from "child_process";
import path from "path";

export async function benefitSearch(text) {
  return new Promise((resolve) => {
    const pyPath = path.resolve("src/python", "benefit_search.py");

    const proc = spawn("python3", [pyPath, text], {
      env: process.env
    });

    let output = "";
    let errorOutput = "";

    proc.stdout.on("data", (data) => {
      output += data.toString();
    });

    proc.stderr.on("data", (data) => {
      errorOutput += data.toString();
    });

    proc.on("close", (code) => {
      // Если Python завершился ошибкой
      if (code !== 0 || errorOutput.trim().length > 0) {
        return resolve({
          ok: false,
          message: "Python error",
          code,
          error: errorOutput.trim()
        });
      }

      // Попытка парсинга JSON
      try {
        const cleanOutput = output.trim();
        const json = JSON.parse(cleanOutput);
        return resolve({
          ok: true,
          data: json
        });
      } catch (err) {
        return resolve({
          ok: false,
          message: "Invalid JSON from Python",
          raw: output.trim(),
          parseError: err.toString()
        });
      }
    });
  });
}