declare module "node:fs" {
    export function readFileSync(path: string, encoding: string): string;
}

declare module "node:path" {
    export function dirname(path: string): string;
    export function join(...parts: string[]): string;
}

declare module "node:url" {
    export function fileURLToPath(url: unknown): string;
}

declare module "node:child_process" {
    export interface SpawnSyncReturns<T> {
        status: number | null;
        stdout: T;
        stderr: T;
        error?: Error;
    }

    export function spawnSync(
        command: string,
        args?: string[],
        options?: { cwd?: string; encoding?: string },
    ): SpawnSyncReturns<string>;
}

declare const process: {
    argv: string[];
    cwd(): string;
    stdout: { write(chunk: string): void };
};
