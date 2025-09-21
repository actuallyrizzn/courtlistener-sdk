<?php

namespace CourtListener\Models;

/**
 * Docket model
 */
class Docket extends BaseModel
{
    /**
     * Get the docket ID
     *
     * @return int|null
     */
    public function getId(): ?int
    {
        return $this->get('id');
    }

    /**
     * Get the case name
     *
     * @return string|null
     */
    public function getCaseName(): ?string
    {
        return $this->get('case_name');
    }

    /**
     * Get the docket number
     *
     * @return string|null
     */
    public function getDocketNumber(): ?string
    {
        return $this->get('docket_number');
    }

    /**
     * Get the court ID
     *
     * @return int|null
     */
    public function getCourtId(): ?int
    {
        return $this->get('court');
    }

    /**
     * Get the court name
     *
     * @return string|null
     */
    public function getCourtName(): ?string
    {
        return $this->get('court_name');
    }

    /**
     * Get the case type
     *
     * @return string|null
     */
    public function getCaseType(): ?string
    {
        return $this->get('case_type');
    }

    /**
     * Get the case type name
     *
     * @return string|null
     */
    public function getCaseTypeName(): ?string
    {
        return $this->get('case_type_name');
    }

    /**
     * Get the date filed
     *
     * @return string|null
     */
    public function getDateFiled(): ?string
    {
        return $this->get('date_filed');
    }

    /**
     * Get the date terminated
     *
     * @return string|null
     */
    public function getDateTerminated(): ?string
    {
        return $this->get('date_terminated');
    }

    /**
     * Get the date last filing
     *
     * @return string|null
     */
    public function getDateLastFiling(): ?string
    {
        return $this->get('date_last_filing');
    }

    /**
     * Get the assigned to
     *
     * @return string|null
     */
    public function getAssignedTo(): ?string
    {
        return $this->get('assigned_to');
    }

    /**
     * Get the referred to
     *
     * @return string|null
     */
    public function getReferredTo(): ?string
    {
        return $this->get('referred_to');
    }

    /**
     * Get the cause
     *
     * @return string|null
     */
    public function getCause(): ?string
    {
        return $this->get('cause');
    }

    /**
     * Get the nature of suit
     *
     * @return string|null
     */
    public function getNatureOfSuit(): ?string
    {
        return $this->get('nature_of_suit');
    }

    /**
     * Get the jury demand
     *
     * @return string|null
     */
    public function getJuryDemand(): ?string
    {
        return $this->get('jury_demand');
    }

    /**
     * Get the jurisdiction type
     *
     * @return string|null
     */
    public function getJurisdictionType(): ?string
    {
        return $this->get('jurisdiction_type');
    }

    /**
     * Get the jurisdiction type name
     *
     * @return string|null
     */
    public function getJurisdictionTypeName(): ?string
    {
        return $this->get('jurisdiction_type_name');
    }

    /**
     * Get the absolute URL
     *
     * @return string|null
     */
    public function getAbsoluteUrl(): ?string
    {
        return $this->get('absolute_url');
    }

    /**
     * Get the resource URI
     *
     * @return string|null
     */
    public function getResourceUri(): ?string
    {
        return $this->get('resource_uri');
    }

    /**
     * Get the date created
     *
     * @return string|null
     */
    public function getDateCreated(): ?string
    {
        return $this->get('date_created');
    }

    /**
     * Get the date modified
     *
     * @return string|null
     */
    public function getDateModified(): ?string
    {
        return $this->get('date_modified');
    }

    /**
     * Get the blocked
     *
     * @return bool|null
     */
    public function getBlocked(): ?bool
    {
        return $this->get('blocked');
    }

    /**
     * Get the appeal from
     *
     * @return string|null
     */
    public function getAppealFrom(): ?string
    {
        return $this->get('appeal_from');
    }

    /**
     * Get the appeal from name
     *
     * @return string|null
     */
    public function getAppealFromName(): ?string
    {
        return $this->get('appeal_from_name');
    }

    /**
     * Get the appeal to
     *
     * @return string|null
     */
    public function getAppealTo(): ?string
    {
        return $this->get('appeal_to');
    }

    /**
     * Get the appeal to name
     *
     * @return string|null
     */
    public function getAppealToName(): ?string
    {
        return $this->get('appeal_to_name');
    }

    /**
     * Get the assigned to name
     *
     * @return string|null
     */
    public function getAssignedToName(): ?string
    {
        return $this->get('assigned_to_name');
    }

    /**
     * Get the referred to name
     *
     * @return string|null
     */
    public function getReferredToName(): ?string
    {
        return $this->get('referred_to_name');
    }

    /**
     * Get the panel
     *
     * @return array|null
     */
    public function getPanel(): ?array
    {
        return $this->get('panel');
    }

    /**
     * Get the panel names
     *
     * @return array|null
     */
    public function getPanelNames(): ?array
    {
        return $this->get('panel_names');
    }

    /**
     * Get the docket entries count
     *
     * @return int|null
     */
    public function getDocketEntriesCount(): ?int
    {
        return $this->get('docket_entries_count');
    }

    /**
     * Get the parties count
     *
     * @return int|null
     */
    public function getPartiesCount(): ?int
    {
        return $this->get('parties_count');
    }

    /**
     * Get the attorneys count
     *
     * @return int|null
     */
    public function getAttorneysCount(): ?int
    {
        return $this->get('attorneys_count');
    }

    /**
     * Get the recap documents count
     *
     * @return int|null
     */
    public function getRecapDocumentsCount(): ?int
    {
        return $this->get('recap_documents_count');
    }

}
