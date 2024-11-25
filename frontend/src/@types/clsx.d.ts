// frontend/src/@types/clsx.d.ts
declare module 'clsx' {
    export type ClassValue = string | number | ClassValue[] | { [key: string]: any };
    export default function clsx(...inputs: ClassValue[]): string;
  }