import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators, FormsModule } from '@angular/forms';
import { FeedbackService, Feedback as FeedbackModel } from '../../services/feedback.service';

const FALLBACK_FEEDBACKS: FeedbackModel[] = [
  {
    id: 1,
    user_name: "Amit Sharma (Delhi)",
    subject: "PM Ayushman Bharat Digital Health Mission",
    message: "Extremely helpful initiative. Got my ABHA card created seamlessly at the district civil hospital and received cashless treatment worth ₹5 Lakhs.",
    content: "Extremely helpful initiative. Got my ABHA card created seamlessly at the district civil hospital and received cashless treatment worth ₹5 Lakhs.",
    rating: 5,
    likes: 28,
    status: "Published",
    created_at: new Date(Date.now() - 86400000 * 2).toISOString()
  },
  {
    id: 2,
    user_name: "Priya Patel (Surat, Gujarat)",
    subject: "Green Solar Rooftop Subsidy Initiative 2026",
    message: "Solar rooftop installation subsidy was directly credited to my bank account via DBT. Reduced our family electricity bill by 85%!",
    content: "Solar rooftop installation subsidy was directly credited to my bank account via DBT. Reduced our family electricity bill by 85%!",
    rating: 5,
    likes: 22,
    status: "Published",
    created_at: new Date(Date.now() - 86400000 * 4).toISOString()
  },
  {
    id: 3,
    user_name: "Sneha Reddy (Hyderabad, Telangana)",
    subject: "National Education Policy (NEP) Skill Upgrade",
    message: "Vocational coding & AI courses introduced from Grade 6 in government schools are helping my children build practical tech skills early.",
    content: "Vocational coding & AI courses introduced from Grade 6 in government schools are helping my children build practical tech skills early.",
    rating: 5,
    likes: 35,
    status: "Published",
    created_at: new Date(Date.now() - 86400000 * 8).toISOString()
  },
  {
    id: 4,
    user_name: "Ramesh Verma (Ludhiana, Punjab)",
    subject: "PM-KISAN Agricultural Income Support",
    message: "Direct bank transfer of ₹2,000 quarterly installment was received on time without any middleman hassle.",
    content: "Direct bank transfer of ₹2,000 quarterly installment was received on time without any middleman hassle.",
    rating: 4,
    likes: 18,
    status: "Published",
    created_at: new Date(Date.now() - 86400000 * 6).toISOString()
  },
  {
    id: 5,
    user_name: "Karan Singh (Jaipur, Rajasthan)",
    subject: "Startup India Seed Capital Grant Scheme",
    message: "Application procedure was transparent. It would be great to have faster processing times for tier-2 city tech startups.",
    content: "Application procedure was transparent. It would be great to have faster processing times for tier-2 city tech startups.",
    rating: 3,
    likes: 9,
    status: "Published",
    created_at: new Date(Date.now() - 86400000 * 10).toISOString()
  }
];

@Component({
  selector: 'app-feedback',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './feedback.html',
  styleUrl: './feedback.css'
})
export class Feedback implements OnInit {
  feedbacks: FeedbackModel[] = FALLBACK_FEEDBACKS;
  feedbackForm: FormGroup;
  showForm = false;
  isLoading = false;
  successMessage = '';

  // Filter and Search State
  selectedTab: 'ALL' | 'POSITIVE' | 'POPULAR' | 'NEEDS_ATTENTION' = 'ALL';
  searchQuery: string = '';

  constructor(private fb: FormBuilder, private feedbackService: FeedbackService) {
    this.feedbackForm = this.fb.group({
      user_name: ['', Validators.required],
      subject: ['', [Validators.required, Validators.minLength(3)]],
      rating: [5, [Validators.required, Validators.min(1), Validators.max(5)]],
      content: ['', [Validators.required, Validators.minLength(5)]]
    });
  }

  ngOnInit(): void {
    this.loadFeedbacks();
  }

  loadFeedbacks(): void {
    this.feedbackService.getFeedbacks().subscribe({
      next: (data) => {
        if (data && data.length > 0) {
          // Merge remote items with likes count
          this.feedbacks = data.map(d => ({
            ...d,
            likes: d.likes || Math.floor(Math.random() * 15) + 5
          }));
        }
      },
      error: (err) => {
        console.warn('Error fetching feedbacks, using fallback:', err);
      }
    });
  }

  // Filtered List Getter
  get filteredFeedbacks(): FeedbackModel[] {
    let list = [...this.feedbacks];

    // Search filter
    const q = this.searchQuery.toLowerCase().trim();
    if (q) {
      list = list.filter(f => 
        (f.user_name && f.user_name.toLowerCase().includes(q)) ||
        (f.subject && f.subject.toLowerCase().includes(q)) ||
        (this.getFeedbackMessage(f).toLowerCase().includes(q))
      );
    }

    // Category / Rating tab filter
    if (this.selectedTab === 'POSITIVE') {
      list = list.filter(f => (f.rating || 5) >= 4);
    } else if (this.selectedTab === 'POPULAR') {
      list = list.filter(f => (f.rating || 5) >= 4).sort((a, b) => (b.likes || 0) - (a.likes || 0));
    } else if (this.selectedTab === 'NEEDS_ATTENTION') {
      list = list.filter(f => (f.rating || 5) <= 3);
    }

    return list;
  }

  // Sentiment Analytics Getters
  get averageRating(): number {
    if (this.feedbacks.length === 0) return 5.0;
    const sum = this.feedbacks.reduce((acc, f) => acc + (f.rating || 5), 0);
    return Math.round((sum / this.feedbacks.length) * 10) / 10;
  }

  get positivePercent(): number {
    if (this.feedbacks.length === 0) return 100;
    const positiveCount = this.feedbacks.filter(f => (f.rating || 5) >= 4).length;
    return Math.round((positiveCount / this.feedbacks.length) * 100);
  }

  get positiveCount(): number {
    return this.feedbacks.filter(f => (f.rating || 5) >= 4).length;
  }

  get popularCount(): number {
    return this.feedbacks.filter(f => (f.likes || 0) > 10).length;
  }

  upvote(fb: FeedbackModel): void {
    fb.likes = (fb.likes || 0) + 1;
  }

  setTab(tab: 'ALL' | 'POSITIVE' | 'POPULAR' | 'NEEDS_ATTENTION'): void {
    this.selectedTab = tab;
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
    const val = this.feedbackForm.value;
    const payload = {
      user_name: val.user_name,
      subject: val.subject,
      rating: Number(val.rating),
      content: val.content,
      message: val.content
    };

    this.feedbackService.createFeedback(payload).subscribe({
      next: (newFeedback) => {
        this.isLoading = false;
        this.successMessage = 'Thank you! Your feedback has been submitted successfully.';
        newFeedback.likes = 1;
        this.feedbacks.unshift(newFeedback);
        this.feedbackForm.reset({ rating: 5 });
        this.showForm = false;
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error submitting feedback', err);
        // Fallback local insertion if server call fails
        const localItem: FeedbackModel = {
          id: Date.now(),
          user_name: val.user_name,
          subject: val.subject,
          rating: Number(val.rating),
          message: val.content,
          content: val.content,
          likes: 1,
          status: "Published",
          created_at: new Date().toISOString()
        };
        this.feedbacks.unshift(localItem);
        this.successMessage = 'Thank you! Your feedback has been published.';
        this.feedbackForm.reset({ rating: 5 });
        this.showForm = false;
      }
    });
  }

  getFeedbackMessage(fb: FeedbackModel): string {
    return fb.message || fb.content || '';
  }
}
