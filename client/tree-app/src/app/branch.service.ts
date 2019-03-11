import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { catchError, map, tap } from 'rxjs/operators';

import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Branch } from './branch';
import { BRANCHES } from './mock-branches';


const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable()
export class BranchService {

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  getBranches(parent: any): Observable<Branch[]> {

    var url = this.branchesUrl;
    if(parent){
        url += `?parent_id=${parent.id}`;
    }

    return this.http.get<Branch[]>(url).pipe(
      catchError(this.handleError('getBranches', []))
    );
  }

  getBranch(id: string): Observable<Branch> {
    const url = `${this.branchUrl}/${id}`;
    return this.http.get<Branch>(url).pipe(
      tap(_ => this.log(`fetched branch id=${id}`)),
      catchError(this.handleError<Branch>(`getBranch id=${id}`))
    );
  }

  constructor(
    private http: HttpClient
  ) { }

  private log(message: string) {
    console.log('BranchService: ' + message);
  }

  private branchesUrl = 'api/branches';
  private branchUrl = 'api/branch';

  /** PUT: update the branch on the server */
  updateBranch (branch: Branch): Observable<any> {
    const url = `${this.branchUrl}/${branch.id}`;

    return this.http.put(url, branch, httpOptions).pipe(
      tap(_ => this.log(`updated branch id=${branch.id}`)),
      catchError(this.handleError<any>('updateBranch'))
    );
  }

  /** POST: add a new branch to the server */
  addBranch (branch: Branch): Observable<Branch> {
    return this.http.post<Branch>(this.branchesUrl, branch, httpOptions).pipe(
      tap((branch: Branch) => this.log(`added branch w/ id=${branch.id}`)),
      catchError(this.handleError<Branch>('addBranch'))
    );
  }

  /** DELETE: delete the hero from the server */
  deleteBranch (branch: Branch | number): Observable<Branch> {
    const id = typeof branch === 'number' ? branch : branch.id;
    const url = `${this.branchUrl}/${id}`;

    return this.http.delete<Branch>(url, httpOptions).pipe(
      tap(_ => this.log(`deleted branch id=${id}`)),
      catchError(this.handleError<Branch>('deleteBranch'))
    );
  }

  /* GET heroes whose name contains search term */
  searchBranches(term: string): Observable<Branch[]> {
    if (!term.trim()) {
      // if not search term, return empty hero array.
      return of([]);
    }
    const url = `${this.branchesUrl}?name=${term}`;

    return this.http.get<Branch[]>(url).pipe(
      tap(_ => this.log(`found branches matching "${term}"`)),
      catchError(this.handleError<Branch[]>('searchBranches', []))
    );
  }

}
