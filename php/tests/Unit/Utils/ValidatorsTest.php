<?php

namespace CourtListener\Tests\Unit\Utils;

use CourtListener\Utils\Validators;
use PHPUnit\Framework\TestCase;

class ValidatorsTest extends TestCase
{
    public function testValidateDate()
    {
        $this->assertTrue(Validators::validateDate('2023-01-01'));
        $this->assertTrue(Validators::validateDate('2023-12-31'));
        $this->assertTrue(Validators::validateDate('2023-02-29')); // Leap year
        $this->assertFalse(Validators::validateDate('2023-13-01')); // Invalid month
        $this->assertFalse(Validators::validateDate('2023-01-32')); // Invalid day
        $this->assertFalse(Validators::validateDate('invalid-date'));
        $this->assertFalse(Validators::validateDate(''));
        $this->assertFalse(Validators::validateDate(null));
    }

    public function testValidateDateWithCustomFormat()
    {
        $this->assertTrue(Validators::validateDate('01/01/2023', 'm/d/Y'));
        $this->assertTrue(Validators::validateDate('31-12-2023', 'd-m-Y'));
        $this->assertFalse(Validators::validateDate('2023-01-01', 'm/d/Y'));
        $this->assertFalse(Validators::validateDate('invalid', 'Y-m-d'));
    }

    public function testValidateCitation()
    {
        $this->assertTrue(Validators::validateCitation('123 U.S. 456'));
        $this->assertTrue(Validators::validateCitation('123 F. 456'));
        $this->assertTrue(Validators::validateCitation('123 F. Supp. 456'));
        $this->assertTrue(Validators::validateCitation('123 Cal. 456'));
        $this->assertTrue(Validators::validateCitation('123 N.Y. 456'));
        $this->assertFalse(Validators::validateCitation('invalid citation'));
        $this->assertFalse(Validators::validateCitation(''));
        $this->assertFalse(Validators::validateCitation(null));
    }

    public function testValidateDocketNumber()
    {
        $this->assertTrue(Validators::validateDocketNumber('1-23-cv-456'));
        $this->assertTrue(Validators::validateDocketNumber('1:23-cv-456'));
        $this->assertTrue(Validators::validateDocketNumber('1-cv-456'));
        $this->assertTrue(Validators::validateDocketNumber('123'));
        $this->assertTrue(Validators::validateDocketNumber('1-23'));
        $this->assertFalse(Validators::validateDocketNumber('invalid-docket'));
        $this->assertFalse(Validators::validateDocketNumber(''));
        $this->assertFalse(Validators::validateDocketNumber(null));
    }

    public function testValidateCourtId()
    {
        $this->assertTrue(Validators::validateCourtId('ca1'));
        $this->assertTrue(Validators::validateCourtId('ca-1'));
        $this->assertTrue(Validators::validateCourtId('ca_1'));
        $this->assertTrue(Validators::validateCourtId('ca1-2'));
        $this->assertTrue(Validators::validateCourtId('123'));
        $this->assertFalse(Validators::validateCourtId('ca@1'));
        $this->assertFalse(Validators::validateCourtId('ca 1'));
        $this->assertFalse(Validators::validateCourtId(''));
        $this->assertFalse(Validators::validateCourtId(null));
    }

    public function testValidateApiToken()
    {
        $this->assertTrue(Validators::validateApiToken('abcdefghijklmnopqrstuvwxyz1234567890'));
        $this->assertTrue(Validators::validateApiToken('12345678901234567890'));
        $this->assertFalse(Validators::validateApiToken('short'));
        $this->assertFalse(Validators::validateApiToken(''));
        $this->assertFalse(Validators::validateApiToken(null));
    }

    public function testValidateId()
    {
        $this->assertTrue(Validators::validateId(123));
        $this->assertTrue(Validators::validateId('123'));
        $this->assertTrue(Validators::validateId(1));
        $this->assertFalse(Validators::validateId(0));
        $this->assertFalse(Validators::validateId(-1));
        $this->assertFalse(Validators::validateId('0'));
        $this->assertFalse(Validators::validateId('-1'));
        $this->assertFalse(Validators::validateId('abc'));
        $this->assertFalse(Validators::validateId(null));
        $this->assertFalse(Validators::validateId([]));
    }

    public function testValidateUrl()
    {
        $this->assertTrue(Validators::validateUrl('https://example.com'));
        $this->assertTrue(Validators::validateUrl('http://example.com'));
        $this->assertTrue(Validators::validateUrl('https://example.com/path'));
        $this->assertTrue(Validators::validateUrl('https://example.com/path?query=1'));
        $this->assertTrue(Validators::validateUrl('https://example.com/path#fragment'));
        $this->assertFalse(Validators::validateUrl('not-a-url'));
        $this->assertFalse(Validators::validateUrl('ftp://example.com'));
        $this->assertFalse(Validators::validateUrl(''));
        $this->assertFalse(Validators::validateUrl(null));
    }

    public function testValidateRequired()
    {
        $this->assertTrue(Validators::validateRequired('valid string'));
        $this->assertTrue(Validators::validateRequired(123));
        $this->assertTrue(Validators::validateRequired(true));
        $this->assertTrue(Validators::validateRequired([1, 2, 3]));
        $this->assertFalse(Validators::validateRequired(''));
        $this->assertFalse(Validators::validateRequired('   '));
        $this->assertFalse(Validators::validateRequired(null));
        $this->assertFalse(Validators::validateRequired([]));
    }

    public function testValidateEmail()
    {
        $this->assertTrue(Validators::validateEmail('test@example.com'));
        $this->assertTrue(Validators::validateEmail('user.name@domain.co.uk'));
        $this->assertTrue(Validators::validateEmail('test+tag@example.org'));
        $this->assertFalse(Validators::validateEmail('invalid-email'));
        $this->assertFalse(Validators::validateEmail('@example.com'));
        $this->assertFalse(Validators::validateEmail('test@'));
        $this->assertFalse(Validators::validateEmail(''));
        $this->assertFalse(Validators::validateEmail(null));
    }

    public function testValidatePhone()
    {
        $this->assertTrue(Validators::validatePhone('1234567890'));
        $this->assertTrue(Validators::validatePhone('(123) 456-7890'));
        $this->assertTrue(Validators::validatePhone('123-456-7890'));
        $this->assertTrue(Validators::validatePhone('123.456.7890'));
        $this->assertTrue(Validators::validatePhone('+1 123 456 7890'));
        $this->assertFalse(Validators::validatePhone('123'));
        $this->assertFalse(Validators::validatePhone('123456789012345'));
        $this->assertFalse(Validators::validatePhone('abc-def-ghij'));
        $this->assertFalse(Validators::validatePhone(''));
        $this->assertFalse(Validators::validatePhone(null));
    }

    public function testValidateCaseName()
    {
        $this->assertTrue(Validators::validateCaseName('Smith v. Jones'));
        $this->assertTrue(Validators::validateCaseName('United States v. Doe'));
        $this->assertTrue(Validators::validateCaseName('ABC Corp. v. XYZ Inc.'));
        $this->assertFalse(Validators::validateCaseName('AB'));
        $this->assertFalse(Validators::validateCaseName('123'));
        $this->assertFalse(Validators::validateCaseName(''));
        $this->assertFalse(Validators::validateCaseName(null));
    }

    public function testValidateJudgeName()
    {
        $this->assertTrue(Validators::validateJudgeName('John Smith'));
        $this->assertTrue(Validators::validateJudgeName('Mary Jane Wilson'));
        $this->assertTrue(Validators::validateJudgeName('Dr. Robert Johnson'));
        $this->assertFalse(Validators::validateJudgeName('John'));
        $this->assertFalse(Validators::validateJudgeName('12345'));
        $this->assertFalse(Validators::validateJudgeName(''));
        $this->assertFalse(Validators::validateJudgeName(null));
    }

    public function testValidateSearchQuery()
    {
        $this->assertTrue(Validators::validateSearchQuery('patent'));
        $this->assertTrue(Validators::validateSearchQuery('copyright law'));
        $this->assertTrue(Validators::validateSearchQuery('Smith v. Jones'));
        $this->assertFalse(Validators::validateSearchQuery('a'));
        $this->assertFalse(Validators::validateSearchQuery(''));
        $this->assertFalse(Validators::validateSearchQuery(null));
    }

    public function testValidatePaginationParams()
    {
        $this->assertTrue(Validators::validatePaginationParams(['page' => 1]));
        $this->assertTrue(Validators::validatePaginationParams(['per_page' => 50]));
        $this->assertTrue(Validators::validatePaginationParams(['page' => 1, 'per_page' => 100]));
        $this->assertFalse(Validators::validatePaginationParams(['page' => 0]));
        $this->assertFalse(Validators::validatePaginationParams(['page' => -1]));
        $this->assertFalse(Validators::validatePaginationParams(['per_page' => 0]));
        $this->assertFalse(Validators::validatePaginationParams(['per_page' => 101]));
        $this->assertTrue(Validators::validatePaginationParams([]));
    }

    public function testValidateDateRangeParams()
    {
        $this->assertTrue(Validators::validateDateRangeParams(['date_created__gte' => '2023-01-01']));
        $this->assertTrue(Validators::validateDateRangeParams(['date_created__lte' => '2023-12-31']));
        $this->assertTrue(Validators::validateDateRangeParams([
            'date_created__gte' => '2023-01-01',
            'date_created__lte' => '2023-12-31'
        ]));
        $this->assertFalse(Validators::validateDateRangeParams(['date_created__gte' => 'invalid-date']));
        $this->assertFalse(Validators::validateDateRangeParams(['date_created__lte' => 'invalid-date']));
        $this->assertFalse(Validators::validateDateRangeParams([
            'date_created__gte' => '2023-12-31',
            'date_created__lte' => '2023-01-01'
        ]));
        $this->assertTrue(Validators::validateDateRangeParams([]));
    }

    public function testValidateFilters()
    {
        $validFilters = [
            'page' => 1,
            'per_page' => 50,
            'q' => 'patent',
            'date_created__gte' => '2023-01-01',
            'date_created__lte' => '2023-12-31'
        ];
        $this->assertTrue(Validators::validateFilters($validFilters));

        $invalidFilters = [
            'page' => 0, // Invalid page
            'q' => 'a'   // Invalid search query
        ];
        $this->assertFalse(Validators::validateFilters($invalidFilters));

        $this->assertTrue(Validators::validateFilters([]));
    }

    public function testEdgeCases()
    {
        // Test with very long strings
        $longString = str_repeat('a', 1000);
        $this->assertTrue(Validators::validateRequired($longString));
        $this->assertTrue(Validators::validateSearchQuery($longString));

        // Test with special characters
        $specialChars = '!@#$%^&*()_+-=[]{}|;:,.<>?';
        $this->assertTrue(Validators::validateRequired($specialChars));

        // Test with unicode characters
        $unicode = '测试中文';
        $this->assertTrue(Validators::validateRequired($unicode));

        // Test with empty arrays
        $this->assertFalse(Validators::validateRequired([]));

        // Test with boolean values
        $this->assertTrue(Validators::validateRequired(true));
        $this->assertTrue(Validators::validateRequired(false));
    }

    public function testComplexValidationScenarios()
    {
        // Valid complex scenario
        $complexValid = [
            'page' => 1,
            'per_page' => 25,
            'q' => 'patent infringement',
            'date_created__gte' => '2023-01-01',
            'date_created__lte' => '2023-12-31',
            'court' => 'ca1',
            'type' => 'opinion'
        ];
        $this->assertTrue(Validators::validateFilters($complexValid));

        // Invalid complex scenario
        $complexInvalid = [
            'page' => -1,
            'per_page' => 150,
            'q' => 'a',
            'date_created__gte' => 'invalid',
            'court' => 'invalid@court'
        ];
        $this->assertFalse(Validators::validateFilters($complexInvalid));
    }
}
