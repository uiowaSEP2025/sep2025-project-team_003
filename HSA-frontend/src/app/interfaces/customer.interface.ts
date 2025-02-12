import {PersonalInformationHelper} from './interface-helpers/personal-information-helper.interface';

export interface Customer extends PersonalInformationHelper {
  customerID: number;
  organizationID: number;
  notes: string;
}
