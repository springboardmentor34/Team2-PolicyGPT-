import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { SchemeService, Scheme } from '../../services/scheme.service';

@Component({
  selector: 'app-scheme-list',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './scheme-list.html',
  styleUrl: './scheme-list.css'
})
export class SchemeList implements OnInit {
  schemes: Scheme[] = [];
  schemeForm: FormGroup;
  showForm = false;
  isEditing = false;
  currentEditingId: number | null = null;
  isLoading = false;

  constructor(private fb: FormBuilder, private schemeService: SchemeService) {
    this.schemeForm = this.fb.group({
      title: ['', Validators.required],
      category: [''],
      department: [''],
      status: ['Active']
    });
  }

  ngOnInit(): void {
    this.loadSchemes();
  }

  loadSchemes(): void {
    this.schemeService.getSchemes().subscribe({
      next: (data) => {
        this.schemes = data;
      },
      error: (err) => console.error(err)
    });
  }

  toggleForm(): void {
    this.showForm = !this.showForm;
    if (!this.showForm) {
      this.resetForm();
    }
  }

  editScheme(scheme: Scheme): void {
    this.isEditing = true;
    this.showForm = true;
    this.currentEditingId = scheme.id;
    this.schemeForm.patchValue({
      title: scheme.title,
      category: scheme.category,
      department: scheme.department,
      status: scheme.status
    });
  }

  deleteScheme(id: number): void {
    if (confirm('Are you sure you want to delete this scheme?')) {
      this.schemeService.deleteScheme(id).subscribe({
        next: () => {
          this.schemes = this.schemes.filter(s => s.id !== id);
        },
        error: (err) => console.error(err)
      });
    }
  }

  onSubmit(): void {
    if (this.schemeForm.invalid) return;

    this.isLoading = true;
    if (this.isEditing && this.currentEditingId) {
      this.schemeService.updateScheme(this.currentEditingId, this.schemeForm.value).subscribe({
        next: (updatedScheme) => {
          const index = this.schemes.findIndex(s => s.id === this.currentEditingId);
          if (index !== -1) {
            this.schemes[index] = updatedScheme;
          }
          this.resetForm();
        },
        error: (err) => {
          console.error(err);
          this.isLoading = false;
        }
      });
    } else {
      this.schemeService.createScheme(this.schemeForm.value).subscribe({
        next: (newScheme) => {
          this.schemes.unshift(newScheme);
          this.resetForm();
        },
        error: (err) => {
          console.error(err);
          this.isLoading = false;
        }
      });
    }
  }

  resetForm(): void {
    this.showForm = false;
    this.isEditing = false;
    this.currentEditingId = null;
    this.isLoading = false;
    this.schemeForm.reset({ status: 'Active' });
  }
}
