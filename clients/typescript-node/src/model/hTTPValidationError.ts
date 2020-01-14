/**
 * MockServer API
 * Simple and fast mock server implemented in python
 *
 * The version of the OpenAPI document: 1.3.6
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { ValidationError } from './validationError';

export class HTTPValidationError {
    'detail'?: Array<ValidationError>;

    static discriminator: string | undefined = undefined;

    static attributeTypeMap: Array<{name: string, baseName: string, type: string}> = [
        {
            "name": "detail",
            "baseName": "detail",
            "type": "Array<ValidationError>"
        }    ];

    static getAttributeTypeMap() {
        return HTTPValidationError.attributeTypeMap;
    }
}

