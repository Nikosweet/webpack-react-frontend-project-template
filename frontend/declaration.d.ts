declare module '*.module.scss' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.png';
declare module '*.jpeg';
declare module '*.jpg';
declare module '*.svg';

declare const __PLATFORM__: 'desktop' | 'mobile'