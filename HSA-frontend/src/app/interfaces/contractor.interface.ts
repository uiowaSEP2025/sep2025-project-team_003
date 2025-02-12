import {PersonalInformationHelper} from './interface-helpers/personal-information-helper.interface';

export interface Contractor extends PersonalInformationHelper {
  contractorID: number;
  organizationID: number;
}
