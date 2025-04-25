import {PersonalInformationHelper} from './interface-helpers/personal-information-helper.interface';

export interface Customer extends PersonalInformationHelper {
  customerID: number;
  organizationID: number;
  notes: string;
}

export interface CustomerParams {
  excludeIDs?: number[];
  search: string,
  pageSize: number,
  offset: number,
}
