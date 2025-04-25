import {PersonalInformationHelper} from './interface-helpers/personal-information-helper.interface';

export interface Contractor extends PersonalInformationHelper {
  contractorID: number;
  organizationID: number;
}

export interface ContractorParams {
  excludeIDs?: number[];
  search: string,
  pageSize: number,
  offset: number,
}
