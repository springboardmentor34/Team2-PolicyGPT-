export interface AppNotification {
  id: number;
  title: string;
  message: string;
  type: 'Policy' | 'Scheme' | 'Deadline' | 'System';
  read: boolean;
  createdAt: string;
}
