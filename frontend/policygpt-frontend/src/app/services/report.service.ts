import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Report {
  id: number;
  title: string;
  content: string;
  created_by: number;
  created_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class ReportService {
  private API_URL = 'http://localhost:8000/reports';

  constructor(private http: HttpClient) {}

  getReports(): Observable<Report[]> {
    return this.http.get<Report[]>(this.API_URL + '/');
  }
}
