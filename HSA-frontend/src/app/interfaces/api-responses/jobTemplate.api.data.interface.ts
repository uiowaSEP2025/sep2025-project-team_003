import {
  ContractorJSON,
  JobTemplateDisplayInterface,
  MaterialJSON,
  ServiceJSON
} from "./jobTemplate.api.display.interface"
import { JobTemplateGeneralDataInterface } from "./jobTemplate.api.general.data.interface"

export interface JobTemplateDataInterface {
    data: JobTemplateGeneralDataInterface,
    services: ServiceJSON[],
    materials: MaterialJSON[],
    contractors: ContractorJSON[],
}
