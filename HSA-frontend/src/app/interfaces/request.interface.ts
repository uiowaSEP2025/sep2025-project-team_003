import {PersonalInformationHelper} from './interface-helpers/personal-information-helper.interface';

export interface Request extends PersonalInformationHelper {
  requestID: number;
  organizationID: number;
  address: string;
  requestDetails: string;
  requestStatus: string;
}

export interface RequestParams {
  excludeIDs?: number[];
  search: string,
  pagesize: number,
  offset: number,
}