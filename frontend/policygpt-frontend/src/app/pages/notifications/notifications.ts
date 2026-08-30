import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NotificationService, Notification } from '../../services/notification.service';

@Component({
  selector: 'app-notifications',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './notifications.html',
  styleUrl: './notifications.css'
})
export class Notifications implements OnInit {
  notifications: Notification[] = [];

  constructor(private notificationService: NotificationService) { }

  ngOnInit(): void {
    this.loadNotifications();
  }

  loadNotifications(): void {
    this.notificationService.getNotifications().subscribe({
      next: (data) => this.notifications = data,
      error: (err) => console.error(err)
    });
  }

  markAsRead(id: number, is_read: boolean): void {
    if (is_read) return;
    this.notificationService.markAsRead(id).subscribe({
      next: () => this.loadNotifications(),
      error: (err) => console.error(err)
    });
  }

  markAllAsRead(): void {
    const hasUnread = this.notifications.some(n => !n.is_read);
    if (!hasUnread) return;

    this.notificationService.markAllAsRead().subscribe({
      next: () => this.loadNotifications(),
      error: (err) => console.error(err)
    });
  }
}
