interface Job {
    id: number;
    jobStatus: string;
    startDate: string;
    endDate: string;
    description: string;
    customerName: string;
    customerID: number;
    requestorAddress: string;
    requestorCity: string;
    requestorState: string;
    requestorZip: string;
}

interface Service {
    id: number;
    serviceID: number;
    serviceName: string;
    serviceDescription: string;
}

interface Material {
    id: number;
    materialID: number;
    materialName: string;
    unitsUsed: number;
    pricePerUnit: number;
}

interface Contractor {
    id: number;
    contractorID: number;
    contractorName: string;
    contractorPhoneNo: string;
    contractorEmail: string;
}


interface JobData {
    data : Job,
    services: Service[],
    materials: Material[],
    contractors: Contractor[]

}

interface Booking {
    id: number;
    event_name: string;
    start_time: string; // ISO datetime string
    end_time: string;   // ISO datetime string
    organization: string;
    booking_type: string;
    back_color: string;
    status: string;
    job: number | null;
  }

export interface BookingFetchResponse {
    event_data: Booking,
    job_data: JobData
}
