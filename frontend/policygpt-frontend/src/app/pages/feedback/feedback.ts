import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { FeedbackService, Feedback as FeedbackModel } from '../../services/feedback.service';

@Component({
  selector: 'app-feedback',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './feedback.html',
  styleUrl: './feedback.css'
})
export class Feedback implements OnInit {
  feedbacks: FeedbackModel[] = [];
  feedbackForm: FormGroup;
  showForm = false;
  isLoading = false;
  successMessage = '';

  constructor(private fb: FormBuilder, private feedbackService: FeedbackService) {
    this.feedbackForm = this.fb.group({
      subject: ['', [Validators.required, Validators.minLength(5)]],
      content: ['', [Validators.required, Validators.minLength(10)]]
    });
  }

  ngOnInit(): void {
    this.loadFeedbacks();
  }

  loadFeedbacks(): void {
    this.feedbackService.getFeedbacks().subscribe({
      next: (data) => {
        this.feedbacks = data;
      },
      error: (err) => {
        console.error('Error fetching feedbacks', err);
      }
    });
  }

  toggleForm(): void {
    this.showForm = !this.showForm;
    this.successMessage = '';
  }

  onSubmit(): void {
    if (this.feedbackForm.invalid) {
      this.feedbackForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.feedbackService.createFeedback(this.feedbackForm.value).subscribe({
      next: (newFeedback) => {
        this.isLoading = false;
        this.successMessage = 'Feedback submitted successfully!';
        this.feedbacks.unshift(newFeedback); // Add to top of list
        this.feedbackForm.reset();
        this.showForm = false;
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error submitting feedback', err);
      }
    });
  }
}
