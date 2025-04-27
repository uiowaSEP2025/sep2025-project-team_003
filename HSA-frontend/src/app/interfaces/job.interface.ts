export interface Job {
  jobID: number;
  organizationID: number;
  customerID: number;
  jobStatus: string;
  jobStartDate: Date;
  jobEndDate: Date;
  jobDescription: string;
}

export interface JobParams {
  excludeIDs?: number[];
  search: string,
  pagesize: number,
  offset: number,
}
