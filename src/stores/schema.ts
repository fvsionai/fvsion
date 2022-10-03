/* tslint:disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type Prompt = string | string[];
export type Unique = string;
/**
 * An enumeration.
 */
export type ModeEnum = "txt2img" | "img2img" | "img2img_inpainting";
export type Name = string;
export type Type = string;
export type Path = string;
export type InitImageBase64 = string;
/**
 * An enumeration.
 */
export type MaskImageEnum = "default" | "alpha" | "white" | "color";
export type MaskColor = string;
export type ApiGithub = string;
export type ApiVersion = string;
export type ModeIschain = boolean;
export type Height = number;
export type Width = number;
export type NumInferenceSteps = number;
export type GuidanceScale = number;
export type Eta = number;
export type Strength = number;
export type Seed = number;
export type Allownsfw = boolean;
export type Pathtolocalmodel = string;
export type Pathtooutput = string;
export type Dojson = boolean;

export interface FvsionModel {
  prompt: Prompt;
  unique?: Unique;
  mode?: ModeEnum & string;
  init_image?: FileModel;
  init_image_base64?: InitImageBase64;
  mask_image_type?: MaskImageEnum & string;
  mask_image?: FileModel;
  mask_color?: MaskColor;
  out_image?: FileModel;
  api_github?: ApiGithub;
  api_version?: ApiVersion;
  mode_isChain?: ModeIschain;
  height?: Height;
  width?: Width;
  num_inference_steps?: NumInferenceSteps;
  guidance_scale?: GuidanceScale;
  eta?: Eta;
  strength?: Strength;
  seed?: Seed;
  allowNSFW?: Allownsfw;
  pathToLocalModel?: Pathtolocalmodel;
  pathToOutput?: Pathtooutput;
  doJSON?: Dojson;
  [k: string]: unknown;
}
export interface FileModel {
  name?: Name;
  type?: Type;
  path?: Path;
  [k: string]: unknown;
}
