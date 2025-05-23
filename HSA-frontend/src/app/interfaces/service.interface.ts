export interface Service {
  serviceID: number;
  organizationID: number;
  serviceName: string;
  serviceDescription: string;
}

export interface ServiceParams {
  excludeIDs?: number[];
  search: string,
  pagesize: number,
  offset: number,
}
