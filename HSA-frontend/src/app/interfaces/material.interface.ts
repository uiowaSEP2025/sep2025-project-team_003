export interface Material {
  materialID: number;
  organizationID: number;
  materialName: string;
}

export interface MaterialParams {
  excludeIDs?: number[];
  search: string,
  pageSize: number,
  offset: number,
}
