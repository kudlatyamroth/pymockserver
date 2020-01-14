/**
 * MockServer API
 * Simple and fast mock server implemented in python
 *
 * The version of the OpenAPI document: 1.3.2
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { HttpRequest } from './httpRequest';
import { HttpResponse } from './httpResponse';

export class CreatePayload {
    'httpRequest': HttpRequest;
    'httpResponse': HttpResponse;

    static discriminator: string | undefined = undefined;

    static attributeTypeMap: Array<{name: string, baseName: string, type: string}> = [
        {
            "name": "httpRequest",
            "baseName": "httpRequest",
            "type": "HttpRequest"
        },
        {
            "name": "httpResponse",
            "baseName": "httpResponse",
            "type": "HttpResponse"
        }    ];

    static getAttributeTypeMap() {
        return CreatePayload.attributeTypeMap;
    }
}

