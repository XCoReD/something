export enum UserRole {
  VIEWER = 'viewer',
  EDITOR = 'editor',
  SUPERVISOR = 'supervisor',
}

export enum VoiceType {
  MALE = 'male',
  FEMALE = 'female',
  ROBOT = 'robot',
  CHILD = 'child',
}

export interface User {
  id: number;
  username: string;
  role: UserRole;
}

export interface ContentItem {
  id: number;
  description: string;
  audioPath?: string;
  order: number;
}

export interface DataUnit {
  id: number;
  order: number;
  isActive: boolean;
  contentItems: ContentItem[];
}

export interface DataUnitStorage {
  id: number;
  name: string;
  voiceType: VoiceType;
  startTime: string;
  breakOnTranslation: boolean;
  isActive: boolean;
  dataUnits: DataUnit[];
}