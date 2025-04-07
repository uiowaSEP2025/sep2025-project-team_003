export interface Material {
  materialID: number;
  organizationID: number;
  materialName: string;
  materialDescription: string;
}

export interface MaterialParams {
  excludeIDs?: number[];
  search: string,
  pagesize: number,
  offset: number,
}
