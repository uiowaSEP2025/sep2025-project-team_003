import { JobTemplateDisplayInterface } from "./jobTemplate.api.display.interface"
import { JobTemplateGeneralDataInterface } from "./jobTemplate.api.general.data.interface"

export interface JobTemplateDataInterface {
    data: JobTemplateGeneralDataInterface,
    services: JobTemplateDisplayInterface,
    materials: JobTemplateDisplayInterface,
    contractors: JobTemplateDisplayInterface,
}