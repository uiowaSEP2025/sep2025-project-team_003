import {Component, Input, OnInit} from '@angular/core';
import {
    MatDialogActions,
    MatDialogClose,
    MatDialogContent,
    MatDialogRef,
    MatDialogTitle
} from "@angular/material/dialog";
import {MatFormField, MatInput, MatLabel} from "@angular/material/input";
import {FormControl, ReactiveFormsModule, Validators} from "@angular/forms";
import {MatButton} from "@angular/material/button";
import {MatError} from "@angular/material/form-field";
import {
    CreateContractorPageComponent
} from "../../contractors/create-contractors-page/create-contractor-page.component";
import {ErrorHandlerService} from "../../../services/error.handler.service";
import {ServiceService} from "../../../services/service.service";
import {Service} from "../../../interfaces/service.interface";

@Component({
  selector: 'app-services-helper',
    imports: [
        MatDialogActions,
        MatDialogClose,
        MatDialogTitle,
        MatError,
        MatFormField,
        MatInput,
        MatLabel,
        ReactiveFormsModule,
        MatDialogContent,
        MatFormField,
        MatButton
    ],
  templateUrl: './services-helper.component.html',
  styleUrl: './services-helper.component.scss'
})
export class ServicesHelperComponent implements OnInit {
    @Input() crudType: 'Create' | 'Update' = 'Create';
    @Input() service!: Service;
    serviceNameControl = new FormControl ('', Validators.required)
    serviceDescriptionControl = new FormControl ('')

    private isFormValid() {
        return this.serviceNameControl.valid
    }

    constructor(public dialogRef: MatDialogRef<CreateContractorPageComponent>,
                private serviceService: ServiceService,
                private errorHandler: ErrorHandlerService) {
    }

    ngOnInit() {
        if (this.crudType === 'Update') {
            this.serviceNameControl = new FormControl (this.service.serviceName, Validators.required)
            this.serviceDescriptionControl = new FormControl (this.service.serviceDescription)
        }

    }

    onSubmit() {
        if (this.isFormValid()) {
            return
        }

        if (this.crudType === 'Update') {
            const args = {
                id: this.service.serviceID,
                service_name: this.serviceNameControl.value,
                service_description: this.serviceDescriptionControl.value
            }

            this.serviceService.editService(args).subscribe(
                {
                    next: () => {
                        this.dialogRef.close();
                        window.location.reload();
                    },
                    error: (error) => {
                        this.errorHandler.handleError(error)
                    }
                }
            )
        } else {
            const args = {
                id: 0,
                service_name: this.serviceNameControl.value,
                service_description: this.serviceDescriptionControl.value
            }
            this.serviceService.createService(args).subscribe(
                {
                    next: () => {
                        this.dialogRef.close();
                        window.location.reload();
                    },
                    error: (error) => {
                        this.errorHandler.handleError(error)
                    }
                }
            )
        }
    }

}
