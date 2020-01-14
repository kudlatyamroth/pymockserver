/**
 * MockServer API
 * Simple and fast mock server implemented in python
 *
 * The version of the OpenAPI document: 1.3.4
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


export class ValidationError {
    'loc': Array<string>;
    'msg': string;
    'type': string;

    static discriminator: string | undefined = undefined;

    static attributeTypeMap: Array<{name: string, baseName: string, type: string}> = [
        {
            "name": "loc",
            "baseName": "loc",
            "type": "Array<string>"
        },
        {
            "name": "msg",
            "baseName": "msg",
            "type": "string"
        },
        {
            "name": "type",
            "baseName": "type",
            "type": "string"
        }    ];

    static getAttributeTypeMap() {
        return ValidationError.attributeTypeMap;
    }
}

