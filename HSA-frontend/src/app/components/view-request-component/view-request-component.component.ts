import { Component, Inject } from '@angular/core';
import { RequestData } from '../../interfaces/api-responses/request.api.interface';
import { RequestService } from '../../services/request.service';
import { Router } from '@angular/router';
import { MAT_DIALOG_DATA, MatDialog, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { LoadingFallbackComponent } from '../loading-fallback/loading-fallback.component';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { AddConfirmDialogComponentComponent } from '../add-confirm-dialog-component/add-confirm-dialog-component.component';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-view-request-component',
  imports: [
    LoadingFallbackComponent, 
    CommonModule, 
    MatButtonModule, 
    MatIconModule, 
    MatCardModule,
    MatListModule,
    MatDividerModule,
    MatDialogModule
  ],
  templateUrl: './view-request-component.component.html',
  styleUrl: './view-request-component.component.scss'
})
export class ViewRequestComponentComponent {
  requestID!: number
  requestData: RequestData | null = null;
  status: string

  constructor(
    private requestService: RequestService,
    private router: Router,
    public dialogRef: MatDialogRef<ViewRequestComponentComponent>,
    public dialog: MatDialog,
    private snackBar: MatSnackBar,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.requestID = data.info.id
    this.status = data.status
  }

  ngOnInit(): void {
    this.requestService.getSpecificRequestData(this.requestID).subscribe(
      {next: (response) => {
        this.requestData = response
        console.log(response)
      },
      error: (error) => {
      }}
    )
  }

  onReturn() {
    this.dialogRef.close(false);
  }

  openApprovalDialog(isApproved: boolean) {
      const dialogRef = this.dialog.open(AddConfirmDialogComponentComponent, {
        width: '300px',
        data: isApproved ? "approval" : "deny"
      });
  
      dialogRef.afterClosed().subscribe((result) => {
        if (result) {
            this.requestService.approveDenyRequest({ id: this.requestID}, isApproved).subscribe({
              next: (response) => {
                this.snackBar.open(isApproved ? 'Approved successfully' : 'Denied successfully', '', {
                  duration: 3000
                });
              }
            })
          window.location.reload();
        }
      })
    }


  navigateToPage(pagePath: string) {
    this.router.navigate([`/${pagePath}`]);
  }
}
