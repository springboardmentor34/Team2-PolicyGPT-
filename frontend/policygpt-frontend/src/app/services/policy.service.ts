import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Policy {
  id: number;
  title: string;
  description: string;
  category: string;
  department: string;
  state: string;
  status: string;
  created_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class PolicyService {
  private API_URL = 'http://localhost:8000/policies';

  constructor(private http: HttpClient) {}

  getPolicies(): Observable<Policy[]> {
    return this.http.get<Policy[]>(this.API_URL + '/');
  }

  getPolicy(id: number): Observable<Policy> {
    return this.http.get<Policy>(`${this.API_URL}/${id}`);
  }

  createPolicy(policy: Partial<Policy>): Observable<Policy> {
    return this.http.post<Policy>(this.API_URL + '/', policy);
  }

  updatePolicy(id: number, policy: Partial<Policy>): Observable<Policy> {
    return this.http.put<Policy>(`${this.API_URL}/${id}`, policy);
  }

  deletePolicy(id: number): Observable<any> {
    return this.http.delete(`${this.API_URL}/${id}`);
  }
}
