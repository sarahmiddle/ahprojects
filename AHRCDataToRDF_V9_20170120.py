# coding: utf-8

# Converting AHRC Data to RDF
# 
# 2016.12.13

# 1. Find each entity in the JSON file and assign it a variable name in Python

# Use safeJSON to import the file and convert it to a Python object (I originally used json but found that it was difficult to deal with values that do not exist - safeJSON resolves this by replacing any nonexistent values with SafeNone).

import safeJSON
from pprint import pprint

import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, XSD
from rdflib.namespace import FOAF, SKOS

from datetime import datetime

#Import namespaces
ukresearchproject = Namespace('http://data.open.ac.uk/ontology/ukresearchproject/')
currency_codes = Namespace('http://reference.data.gov.uk/def/currency/')
dataopen = Namespace('http://data.open.ac.uk/meta/ontology/')
dc = Namespace('http://purl.org/dc/terms/')
doap = Namespace('http://usefulinc.com/ns/doap#')
fabio = Namespace('http://purl.org/spar/fabio/') 
frapo = Namespace('http://purl.org/cerif/frapo/') 
gr = Namespace('http://purl.org/goodrelations/v1#')
org = Namespace('http://www.w3.org/ns/org#')
prism = Namespace('http://prismstandard.org/namespaces/basic/2.0/')  
projectfunding = Namespace("http://vocab.ox.ac.uk/projectfunding#")
vcard = Namespace('http://www.w3.org/2006/vcard/ns#')
vivo = Namespace('http://vivoweb.org/ontology/core#')

ukresearchproject_ontology_uri = 'http://data.open.ac.uk/ontology/ukresearchproject/'

#Define variable for the graph:
g = Graph()

for x in range (1,5440):
    x = str(x)
    json_file = 'json_files/file' + x + '.json'

    with open(json_file) as data_file:    
        data = safeJSON.load(data_file)

# Project URI
# Identify the element for the project's ID (projectOverview.projectComposition.project.id), and assign it to the variable project_id:

    project_id = data['projectOverview']['projectComposition']['project']['id']

# Construct the project's URI:

    ahproject_base_uri = 'http://data.open.ac.uk/ahproject/'
    if (type(project_id) != safeJSON.SafeNoneClass):
        project_uri = ahproject_base_uri + 'project/' + project_id

# Terms directly linked to Project

# Title
# Identify the element for the project's title (projectOverview.projectComposition.project.title), and assign it to the variable project_title:

        project_title = data['projectOverview']['projectComposition']['project']['title']

# Status
# Identify the element for the project's status (projectOverview.projectComposition.project.status), and assign it to the variable project_status:

        project_status = data['projectOverview']['projectComposition']['project']['status']

# Abstract
# Identify the element for the project's abstract (projectOverview.projectComposition.project.abstract), and assign it to the variable project_abstract:

        project_abstract = data['projectOverview']['projectComposition']['project']['abstractText']

# URL
# Identify the element for the project's URL (projectOverview.projectComposition.project.url), and assign it to the variable project_url:

        project_url = data['projectOverview']['projectComposition']['project']['url']

# Potential impact
# Identify the element for the project's potential impact (projectOverview.projectComposition.project.potentialImpactText), and assign it to the variable project_potential_impact:

        project_potential_impact = data['projectOverview']['projectComposition']['project']['potentialImpactText']

# Project identifier (NB this is always the same as the Grant reference)
# Identify the element for the project identifier (projectOverview.projectComposition.project.identifier.value), and assign it to the variable project_identifier:

        project_identifiers = data['projectOverview']['projectComposition']['project']['identifier']

# We can then iterate through these lists in a for loop and convert the results to RDF, as shown in section 2, below.

# ###Subject and Topic Keywords
# Define the list variables 'research_topics' and 'research_subjects':

        research_topics = data['projectOverview']['projectComposition']['project']['researchTopic']

        research_subjects = data['projectOverview']['projectComposition']['project']['researchSubject']

# We can then iterate through these lists in a for loop and convert the results to RDF, as shown in section 2, below.

# Fund and related terms

# Fund
# Construct a URI for 'fund':

        fund_uri = project_uri + '#fund'

# Identify the element for the fund type (projectOverview.projectComposition.project.fund.type), and assign it to the variable fund_type:

        fund_type = data['projectOverview']['projectComposition']['project']['fund']['type']

# Grant reference
# Identify the element for the project's grant reference (projectOverview.projectComposition.project.grantReference), and assign it to the variable grant_reference:

        grant_reference = data['projectOverview']['projectComposition']['project']['grantReference']

# Grant category
# Identify the element for the project's grant category (projectOverview.projectComposition.project.grantCategory), and assign it to the variable grant_category:

        grant_category = data['projectOverview']['projectComposition']['project']['grantCategory']

# Start date
# Identify the element for the project's start date (projectOverview.projectComposition.project.fund.start), and assign it to the variable fund_start:

        fund_start = data['projectOverview']['projectComposition']['project']['fund']['start']

# Convert fund_start from a string to a datetime object:

        fund_start_datetime = datetime.strptime(fund_start,'%Y-%m-%d')

# End date
# Identify the element for the project's end date (projectOverview.projectComposition.project.fund.end), and assign it to the variable fund_end:

        fund_end = data['projectOverview']['projectComposition']['project']['fund']['end']

# Convert fund_end from a string to a datetime object:

        fund_end_datetime = datetime.strptime(fund_end,'%Y-%m-%d')

    # Amount
# Identify the element for the fund amount (projectOverview.projectComposition.project.fund.valuePounds), and assign it to the variable fund_amount:

        fund_amount = data['projectOverview']['projectComposition']['project']['fund']['valuePounds']


# Funder and related terms

# Funder
# Construct a URI for 'funder':
# Identify the element for the project's funder ID (projectOverview.projectComposition.project.fund.funder.id), and assign it to the variable funder_id:

        funder_id = data['projectOverview']['projectComposition']['project']['fund']['funder']['id']

# Build the URI funder_uri using the base URI for AHProject, and specifying that it refers to an organisation:

        funder_uri = ahproject_base_uri + 'organisation/' + funder_id

# Funder name

# Identify the element for the project's funder name (projectOverview.projectComposition.project.fund.funder.name), and assign it to the variable funder_name:

        funder_name = data['projectOverview']['projectComposition']['project']['fund']['funder']['name']

# Funder URL

# Identify the element for the project's funder URL (projectOverview.projectComposition.project.fund.funder.url), and assign it to the variable funder_url:

        funder_url = data['projectOverview']['projectComposition']['project']['fund']['funder']['url']

# Lead Research Organisation and related terms

# Lead Research Organisation
# Construct a URI for 'Lead Research Organisation', by extracting the ID and using the AHProject base URI:

        lead_research_org_id = data['projectOverview']['projectComposition']['leadResearchOrganisation']['id']

        lead_research_org_uri = ahproject_base_uri + 'organisation/' + lead_research_org_id

# Lead Research Organisation Name
# Identify the element for the lead research organisation's name (projectOverview.projectComposition.leadResearchOrganization.name), and assign it to the variable lead_research_org_name:

        lead_research_org_name = data['projectOverview']['projectComposition']['leadResearchOrganisation']['name']

# Department
# Identify the element for the department (projectOverview.projectComposition.leadResearchOrganization.department), and assign it to the variable lead_research_org_dept:

        lead_research_org_dept = data['projectOverview']['projectComposition']['leadResearchOrganisation']['department']

# Lead Research Organisation Type
# Identify the element for the type of lead research organisation (projectOverview.projectComposition.leadResearchOrganization.typeInd), and assign it to the variable lead_research_org_type:

        lead_research_org_type = data['projectOverview']['projectComposition']['leadResearchOrganisation']['typeInd']

# Lead Research Organisation URL
# Identify the element for the lead research organisation's URL (projectOverview.projectComposition.leadResearchOrganization.url), and assign it to the variable lead_research_org_url:

        lead_research_org_url = data['projectOverview']['projectComposition']['leadResearchOrganisation']['url']

# Lead Research Organisation Address
# Construct the URI for the lead research organisation's address:

        lead_research_org_address_uri = lead_research_org_uri + '#address'

# Address Lines 1-5
# Identify the elements for lines 1-5 of the lead research organisation's address (projectOverview.projectComposition.leadResearchOrganization.address.line1-projectOverview.projectComposition.leadResearchOrganization.address.line5), and assigning them to the variables lead_research_org_address_line1-lead_research_org_address_line5:

        lead_research_org_address_line1 = data['projectOverview']['projectComposition']['leadResearchOrganisation']['address']['line1']
        lead_research_org_address_line2 = data['projectOverview']['projectComposition']['leadResearchOrganisation']['address']['line2']
        lead_research_org_address_line3 = data['projectOverview']['projectComposition']['leadResearchOrganisation']['address']['line3']
        lead_research_org_address_line4 = data['projectOverview']['projectComposition']['leadResearchOrganisation']['address']['line4']
        lead_research_org_address_line5 = data['projectOverview']['projectComposition']['leadResearchOrganisation']['address']['line5']

# Construct a string that concatenates all existing values:

        lead_research_org_address_lines = ''
        if (type(lead_research_org_address_line1) != safeJSON.SafeNoneClass):
            lead_research_org_address_lines = lead_research_org_address_lines + lead_research_org_address_line1
            if ((type(lead_research_org_address_line2) != safeJSON.SafeNoneClass) or (type(lead_research_org_address_line3) != safeJSON.SafeNoneClass) or (type(lead_research_org_address_line4) != safeJSON.SafeNoneClass) or (type(lead_research_org_address_line5) != safeJSON.SafeNoneClass)):
                lead_research_org_address_lines = lead_research_org_address_lines + ', '
        if (type(lead_research_org_address_line2) != safeJSON.SafeNoneClass):
            lead_research_org_address_lines = lead_research_org_address_lines + lead_research_org_address_line2
            if ((type(lead_research_org_address_line3) != safeJSON.SafeNoneClass) or (type(lead_research_org_address_line4) != safeJSON.SafeNoneClass) or (type(lead_research_org_address_line5) != safeJSON.SafeNoneClass)):
                lead_research_org_address_lines = lead_research_org_address_lines + ', '
        if (type(lead_research_org_address_line3) != safeJSON.SafeNoneClass):
            lead_research_org_address_lines = lead_research_org_address_lines + lead_research_org_address_line3
            if ((type(lead_research_org_address_line4) != safeJSON.SafeNoneClass) or (type(lead_research_org_address_line5) != safeJSON.SafeNoneClass)):
                lead_research_org_address_lines = lead_research_org_address_lines + ', '
        if (type(lead_research_org_address_line4) != safeJSON.SafeNoneClass):
            lead_research_org_address_lines = lead_research_org_address_lines + lead_research_org_address_line4
            if (type(lead_research_org_address_line5) != safeJSON.SafeNoneClass):
                lead_research_org_address_lines = lead_research_org_address_lines + ', '
        if (type(lead_research_org_address_line5) != safeJSON.SafeNoneClass):
            lead_research_org_address_lines = lead_research_org_address_lines + lead_research_org_address_line5

# Replace special characters resulting from line breaks in the original text with commas:

        lead_research_org_address_lines = lead_research_org_address_lines.replace("\r\n", ", ")

# Postcode
# Identify the element for the lead research organisation's postcode (projectOverview.projectComposition.leadResearchOrganization.address.postCode), and assign it to the variable lead_research_org_postcode:

        lead_research_org_postcode = data['projectOverview']['projectComposition']['leadResearchOrganisation']['address']['postCode']

# Region
# Identify the element for the lead research organisation's region (projectOverview.projectComposition.leadResearchOrganization.address.region), and assign it to the variable lead_research_org_region:

        lead_research_org_region = data['projectOverview']['projectComposition']['leadResearchOrganisation']['address']['region']

# Country
# Identify the element for the lead research organisation's country (projectOverview.projectComposition.leadResearchOrganization.address.country), and assign it to the variable lead_research_org_country:

        lead_research_org_country = data['projectOverview']['projectComposition']['leadResearchOrganisation']['address']['country']

# Person and related terms

# Define the 'people' object:

        people = data['projectOverview']['projectComposition']['personRole']

# Identify the role for each person:

        for person in people:
            person_role = person['role']

# Identify the name of each role:

        for role in person_role:
            person_role_name = role['name']

# We can then iterate through this object in a for loop and convert the results to RDF, as shown in section 2, below.

# Publication and related terms
# Define the 'publications' object:

        publications = data['projectOverview']['projectComposition']['project']['publication']

# Where there are no publications, the value of publications is '[]'. The type of the publications object is always safeJSON.SafeList.
# We can then iterate through this object in a for loop and convert the results to RDF, as shown in section 2, below.

# Collaborating Organisations and related terms

# Define the 'collaborators' object:

        collaborators = data['projectOverview']['projectComposition']['collaborator']

# We can then iterate through this object in a for loop and convert the results to RDF, as shown in section 2, below.

# Outputs

# Define the 'outputs' object:

        outputs = data['projectOverview']['projectComposition']['project']['output']

# We can then iterate through these objects in a for loop and convert the results to RDF, as shown in section 2, below.

# 2. Use RDFLib to construct relationships between variables from the JSON file and external ontologies

#Convert the URI variables defined above into URI references:
        project = URIRef(project_uri)
        fund = URIRef(fund_uri)
        funder = URIRef(funder_uri)
        lead_research_org = URIRef(lead_research_org_uri)
        lead_research_org_address = URIRef(lead_research_org_address_uri)

# Add triples using store's add method.

#Terms directly linked to Project
        g.add( (project, RDF.type, projectfunding.Project ))
        if (type(project_url) != safeJSON.SafeNoneClass):
            g.add( (project, FOAF.homepage, Literal(project_url,datatype=XSD.string) ))
        if (type(project_status) != safeJSON.SafeNoneClass):
            g.add( (project, dataopen.status, Literal(project_status,datatype=XSD.string) ))
        if (type(project_title) != safeJSON.SafeNoneClass):
            g.add( (project, dc.title, Literal(project_title,datatype=XSD.string) ))
        if (type(project_abstract) != safeJSON.SafeNoneClass):
            g.add( (project, dc.abstract, Literal(project_abstract,datatype=XSD.string) ))
        if (type(project_potential_impact) != safeJSON.SafeNoneClass):
            g.add( (project, ukresearchproject.potentialImpact, Literal(project_potential_impact,datatype=XSD.string) ))
        for project_identifier in project_identifiers:
            project_identifier_value = project_identifier['value']
            if (type(project_identifier_value) != safeJSON.SafeNoneClass):
                g.add( (project, frapo.hasProjectIdentifier, Literal(project_identifier_value,datatype=XSD.string) ))

#Subject and Topic keywords
        for research_topic in research_topics:
            research_topic_id = research_topic['id']
            research_topic_text = research_topic['text']
            if (type(research_topic_id) != safeJSON.SafeNoneClass):
                research_topic_uri_string = ahproject_base_uri + 'topic/' + research_topic_id
                research_topic_uri = URIRef(research_topic_uri_string)
                g.add( (research_topic_uri, RDF.type, SKOS.Concept ))
                g.add( (project, dc.subject, research_topic_uri ))
                if (type(research_topic_text) != safeJSON.SafeNoneClass):
                    g.add( (research_topic_uri, SKOS.prefLabel, Literal(research_topic_text,datatype=XSD.string) ))

        for research_subject in research_subjects:
            research_subject_id = research_subject['id']
            research_subject_text = research_subject['text']
            if (type(research_subject_id) != safeJSON.SafeNoneClass):
                research_subject_uri_string = ahproject_base_uri + 'subject/' + research_subject_id
                research_subject_uri = URIRef(research_subject_uri_string)  
                g.add( (research_subject_uri, RDF.type, SKOS.Concept ))
                g.add( (project, dc.subject, research_subject_uri ))
                if (type(research_subject_text) != safeJSON.SafeNoneClass):
                    g.add( (research_subject_uri, SKOS.prefLabel, Literal(research_subject_text,datatype=XSD.string) ))

#Fund and related terms
        g.add( (fund, RDF.type, projectfunding.Funding ))
        g.add( (fund, projectfunding.funds, project ))
        g.add( (fund, projectfunding.grantNumber, Literal(grant_reference,datatype=XSD.string) ))
        if (type(fund_type) != safeJSON.SafeNoneClass):
            g.add( (fund, gr.category, Literal(fund_type,datatype=XSD.string) ))
        if (type(grant_category) != safeJSON.SafeNoneClass):
            g.add( (fund, doap.category, Literal(grant_category,datatype=XSD.string) ))
        if (type(fund_amount) != safeJSON.SafeNoneClass):
            g.add( (fund, frapo.hasMonetaryValue, Literal(fund_amount,datatype=XSD.decimal) ))
            g.add( (fund, frapo.hasCurrencyCode, currency_codes.GBP ))
        g.add( (fund, projectfunding.startDate, Literal(fund_start_datetime,datatype=XSD.dateTime) ))
        g.add( (fund, projectfunding.endDate, Literal(fund_end_datetime,datatype=XSD.dateTime) ))

#Funder and related terms
        g.add( (funder, RDF.type, projectfunding.FundingBody ))
        g.add( (funder, projectfunding.provides, fund ))
        if (type(funder_name) != safeJSON.SafeNoneClass):
            g.add( (funder, vcard.hasOrganizationName, Literal(funder_name,datatype=XSD.string) ))
        if (type(funder_url) != safeJSON.SafeNoneClass):
            g.add( (funder, FOAF.homepage, Literal(funder_url,datatype=XSD.string) ))

#Lead Research Organisation and related terms
        g.add( (lead_research_org, RDF.type, org.Organization ))
        g.add( (lead_research_org, org.HeadOf, project ))
        if (type(lead_research_org_name) != safeJSON.SafeNoneClass):
            g.add( (lead_research_org, vcard.hasOrganizationName, Literal(lead_research_org_name,datatype=XSD.string) ))
        if (type(lead_research_org_dept) != safeJSON.SafeNoneClass):
            g.add( (lead_research_org, vcard.hasOrganizationUnit, Literal(lead_research_org_dept,datatype=XSD.string) ))
        if (type(lead_research_org_type) != safeJSON.SafeNoneClass):
            g.add( (lead_research_org, org.classification, Literal(lead_research_org_type,datatype=XSD.string) ))
        if (type(lead_research_org_url) != safeJSON.SafeNoneClass):
            g.add( (lead_research_org, FOAF.homepage, Literal(lead_research_org_url,datatype=XSD.string) ))
        g.add( (lead_research_org, org.siteAddress, lead_research_org_address ))
        g.add( (lead_research_org_address, RDF.type, vcard.Address ))
        if (type(lead_research_org_address_lines) != safeJSON.SafeNoneClass):
            g.add( (lead_research_org_address, frapo.hasPostalAddressLine, Literal(lead_research_org_address_lines,datatype=XSD.string) ))
        if (type(lead_research_org_postcode) != safeJSON.SafeNoneClass):
            g.add( (lead_research_org_address, vcard.hasPostalCode, Literal(lead_research_org_postcode,datatype=XSD.string) ))
        if (type(lead_research_org_region) != safeJSON.SafeNoneClass):
            g.add( (lead_research_org_address, vcard.region, Literal(lead_research_org_region,datatype=XSD.string) ))
        if (type(lead_research_org_country) != safeJSON.SafeNoneClass):
            g.add( (lead_research_org_address, vcard.hasCountryName, Literal(lead_research_org_country,datatype=XSD.string) ))

#People
        for person in people:
            person_id = person['id']
            person_firstname = person['firstName']
            person_surname = person['surname']
            person_orcid = person['orcidId']
            person_url = person['url']
            person_role = person['role']
            if (type(person_id) != safeJSON.SafeNoneClass):
                person_uri_string = ahproject_base_uri + 'person/' + person_id
                person_uri = URIRef(person_uri_string)
                for role in person_role:
                    person_role_name = role['name']
                    if (type(person_role_name) != safeJSON.SafeNoneClass):
                        if (person_role_name == 'PRINCIPAL_INVESTIGATOR'):
                            g.add( (project, projectfunding.hasPrincipalInvestigator, person_uri ))
                        else:
                            g.add( (project, projectfunding.hasCoInvestigator, person_uri ))
                g.add( (person_uri, RDF.type, FOAF.Person ))
                if (type(person_firstname) != safeJSON.SafeNoneClass):
                    g.add( (person_uri, FOAF.givenName, Literal(person_firstname,datatype=XSD.string) ))
                if (type(person_surname) != safeJSON.SafeNoneClass):
                    g.add( (person_uri, FOAF.familyName, Literal(person_surname,datatype=XSD.string) ))
                if (type(person_url) != safeJSON.SafeNoneClass):
                    g.add( (person_uri, FOAF.homepage, Literal(person_url,datatype=XSD.string) ))
                if (type(person_orcid) != safeJSON.SafeNoneClass):
                    person_orcid_uri_string = 'http://orcid.org/' + person_orcid
                    person_orcid_uri = URIRef(person_orcid_uri_string)
                    g.add( (person_uri, frapo.hasORCID, person_orcid_uri ))

#Publications
        for publication in publications:
            publication_id = publication['id']
            publication_title = publication['title']
            publication_url = publication['url']
            publication_parent = publication['parentPublicationTitle']
            publication_isbn = publication['isbn']
            publication_date_str = publication['date']
            publication_first_author = publication['firstAuthorName']
            publication_authors = publication['author']
            if (type(publication_id) != safeJSON.SafeNoneClass):
                publication_uri_string = ahproject_base_uri + 'publication/' + publication_id
                publication_uri = URIRef(publication_uri_string)
                g.add( (project, frapo.hasOutput, publication_uri ))
                g.add( (publication_uri, RDF.type, dc.BibliographicResource ))
                if (type(publication_title) != safeJSON.SafeNoneClass):
                    g.add( (publication_uri, dc.title, Literal(publication_title,datatype=XSD.string) ))
                if (type(publication_url) != safeJSON.SafeNoneClass):
                    g.add( (publication_uri, fabio.hasURL, Literal(publication_url,datatype=XSD.string) ))
                if (type(publication_parent) != safeJSON.SafeNoneClass):
                    g.add( (publication_uri, dc.isPartOf, Literal(publication_parent,datatype=XSD.string) ))
                if (type(publication_isbn) != safeJSON.SafeNoneClass):
                    g.add( (publication_uri, prism.isbn, Literal(publication_isbn,datatype=XSD.string) ))
                if (type(publication_date_str) != safeJSON.SafeNoneClass):
                    publication_date = datetime.strptime(publication_date_str,'%Y-%m-%d')
                    g.add( (publication_uri, dc.issued, Literal(publication_date,datatype=XSD.dateTime) ))
                if (type(publication_first_author) != safeJSON.SafeNoneClass):
                    g.add( (publication_uri, ukresearchproject.authorString, Literal(publication_first_author,datatype=XSD.string) ))
                if (type(publication_authors) != safeJSON.SafeNoneClass):
                    for publication_author in publication_authors:
                        publication_author_other = publication_author['otherNames']
                        if (type(publication_author_other) != safeJSON.SafeNoneClass):
                            g.add( (publication_uri, ukresearchproject.authorString, Literal(publication_author_other,datatype=XSD.string) ))
        
#Collaborating Organisations
        for collab_org in collaborators:
            collab_org_id = collab_org['id']
            collab_org_name = collab_org['name']
            collab_org_url = collab_org['url']
            collab_org_address_line1 = collab_org['address']['line1']
            collab_org_address_line2 = collab_org['address']['line2']
            collab_org_address_line3 = collab_org['address']['line3']
            collab_org_address_line4 = collab_org['address']['line4']
            collab_org_address_line5 = collab_org['address']['line5']
            collab_org_postcode = collab_org['address']['postCode']
            collab_org_region = collab_org['address']['region']
            collab_org_country = collab_org['address']['country']
            if (type(collab_org_id) != safeJSON.SafeNoneClass):
                collab_org_uri_string = ahproject_base_uri + 'organisation/' + collab_org_id
                collab_org_uri = URIRef(collab_org_uri_string)
                g.add( (project, vivo.hasCollaborator, collab_org_uri ))
                g.add( (collab_org_uri, RDF.type, org.Organization ))
                if (type(collab_org_name) != safeJSON.SafeNoneClass):
                    g.add( (collab_org_uri, vcard.hasOrganizationName, Literal(collab_org_name,datatype=XSD.string) ))
                if (type(collab_org_url) != safeJSON.SafeNoneClass):
                    g.add( (collab_org_uri, FOAF.homepage, Literal(collab_org_url,datatype=XSD.string) ))
                if ((type(collab_org_address_line1) != safeJSON.SafeNoneClass) or (type(collab_org_address_line2) != safeJSON.SafeNoneClass) or (type(collab_org_address_line3) != safeJSON.SafeNoneClass) or (type(collab_org_address_line4) != safeJSON.SafeNoneClass) or (type(collab_org_address_line5) != safeJSON.SafeNoneClass) or (type(collab_org_postcode) != safeJSON.SafeNoneClass) or (type(collab_org_region) != safeJSON.SafeNoneClass) or (type(collab_org_country) != safeJSON.SafeNoneClass)):
                    collab_org_address_uri_string = collab_org_uri_string + '#address'
                    collab_org_address_uri = URIRef(collab_org_address_uri_string)
                    g.add( (collab_org_uri, org.siteAddress, collab_org_address_uri ))
                    g.add( (collab_org_address_uri, RDF.type, vcard.Address ))
                    if ((type(collab_org_address_line1) != safeJSON.SafeNoneClass) or (type(collab_org_address_line2) != safeJSON.SafeNoneClass) or (type(collab_org_address_line3) != safeJSON.SafeNoneClass) or (type(collab_org_address_line4) != safeJSON.SafeNoneClass) or (type(collab_org_address_line5) != safeJSON.SafeNoneClass)):
                        collab_org_address_lines = ''
                        if (type(collab_org_address_line1) != safeJSON.SafeNoneClass):
                            collab_org_address_lines = collab_org_address_lines + collab_org_address_line1
                            if ((type(collab_org_address_line2) != safeJSON.SafeNoneClass) or (type(collab_org_address_line3) != safeJSON.SafeNoneClass) or (type(collab_org_address_line4) != safeJSON.SafeNoneClass) or (type(collab_org_address_line5) != safeJSON.SafeNoneClass)):
                                collab_org_address_lines = collab_org_address_lines + ', '
                        if (type(collab_org_address_line2) != safeJSON.SafeNoneClass):
                            collab_org_address_lines = collab_org_address_lines + collab_org_address_line2
                            if ((type(collab_org_address_line3) != safeJSON.SafeNoneClass) or (type(collab_org_address_line4) != safeJSON.SafeNoneClass) or (type(collab_org_address_line5) != safeJSON.SafeNoneClass)):
                                collab_org_address_lines = collab_org_address_lines + ', '
                        if (type(collab_org_address_line3) != safeJSON.SafeNoneClass):
                            collab_org_address_lines = collab_org_address_lines + collab_org_address_line3
                            if ((type(collab_org_address_line4) != safeJSON.SafeNoneClass) or (type(collab_org_address_line5) != safeJSON.SafeNoneClass)):
                                collab_org_address_lines = collab_org_address_lines + ', '
                        if (type(collab_org_address_line4) != safeJSON.SafeNoneClass):
                            collab_org_address_lines = collab_org_address_lines + collab_org_address_line4
                            if (type(collab_org_address_line5) != safeJSON.SafeNoneClass):
                                collab_org_address_lines = collab_org_address_lines + ', '
                        if (type(collab_org_address_line5) != safeJSON.SafeNoneClass):
                            collab_org_address_lines = collab_org_address_lines + collab_org_address_line5
                        collab_org_address_lines = collab_org_address_lines.replace("\r\n", ", ")
                        g.add( (collab_org_address_uri, frapo.hasPostalAddressLine, Literal(collab_org_address_lines,datatype=XSD.string) ))
                    if (type(collab_org_postcode) != safeJSON.SafeNoneClass):
                        g.add( (collab_org_address_uri, vcard.hasPostalCode, Literal(collab_org_postcode,datatype=XSD.string) ))
                    if (type(collab_org_region) != safeJSON.SafeNoneClass):
                        g.add( (collab_org_address_uri, vcard.region, Literal(collab_org_region,datatype=XSD.string) ))
                    if (type(collab_org_country) != safeJSON.SafeNoneClass):
                        g.add( (collab_org_address_uri, vcard.hasCountryName, Literal(collab_org_country,datatype=XSD.string) ))

#Outputs
        for output_category in outputs:
# The JSON syntax for keyFindingsOutput renders it as a dictionary rather than a list, presumably because only one key findings output is permitted. This means it needs to be treated differently from the other output categories.
            if (output_category == 'keyFindingsOutput'):
                key_findings = data['projectOverview']['projectComposition']['project']['output']['keyFindingsOutput']
                output_id = key_findings['id']
                if (type(output_id) != safeJSON.SafeNoneClass):
                    output_uri_string = ahproject_base_uri + 'output/' + output_id
                    output_uri = URIRef(output_uri_string)
                    g.add( (project, frapo.hasOutput, output_uri ))
                    output_class = 'KeyFindingsOutput'
                    output_class_uri_string = ukresearchproject_ontology_uri + output_class
                    output_class_uri = URIRef(output_class_uri_string)
                    g.add( (output_uri, RDF.type, output_class_uri ))
                    output_description= key_findings['description']
                    if (type(output_description) != safeJSON.SafeNoneClass):
                        g.add( (output_uri, dc.description, Literal(output_description,datatype=XSD.string )))
                    output_sectors = key_findings['sector']
                    if (type(output_sectors) != safeJSON.SafeNoneClass):
                        for output_sectors_string in output_sectors:
                            output_sectors_string = output_sectors_string.replace("/ ", ", ")
                            output_sectors_string = output_sectors_string.replace(", ", "- ")
                            output_sectors_string = output_sectors_string.replace(",", ";")
                            output_sectors_string = output_sectors_string.replace("- ", ", ")
                            output_sectors_list = output_sectors_string.split(";")
                            for output_sector in output_sectors_list:
                                g.add( (output_uri, ukresearchproject.sector, Literal(output_sector,datatype=XSD.string )))
                    output_exploitation_pathways = key_findings['exploitationPathways']
                    if (type(output_exploitation_pathways) != safeJSON.SafeNoneClass):
                        g.add( (output_uri, ukresearchproject.exploitationPathways, Literal(output_exploitation_pathways,datatype=XSD.string )))
            if (output_category != 'keyFindingsOutput'):
                output_list = outputs[output_category]
                for output in output_list:
                    output_id = output['id']
                    if (type(output_id) != safeJSON.SafeNoneClass):
                        output_uri_string = ahproject_base_uri + 'output/' + output_id
                        output_uri = URIRef(output_uri_string)
                        g.add( (project, frapo.hasOutput, output_uri ))
                        output_class = output_category[0].upper() + output_category[1:]
                        output_class_uri_string = ukresearchproject_ontology_uri + output_class
                        output_class_uri = URIRef(output_class_uri_string)
                        g.add( (output_uri, RDF.type, output_class_uri ))
                        output_description = output['description']
                        if (type(output_description) != safeJSON.SafeNoneClass):
                            g.add( (output_uri, dc.description, Literal(output_description,datatype=XSD.string )))
                        output_title = output['title']
                        if (type(output_title) != safeJSON.SafeNoneClass):
                            g.add( (output_uri, dc.title, Literal(output_title,datatype=XSD.string )))
                        output_impact = output['impact']
                        if (type(output_impact) != safeJSON.SafeNoneClass):
                            g.add( (output_uri, ukresearchproject.impact, Literal(output_impact,datatype=XSD.string )))
                        output_url = output['url']
                        if (type(output_url) != safeJSON.SafeNoneClass):
                            g.add( (output_uri, FOAF.homepage, Literal(output_url,datatype=XSD.string )))
                        output_type = output['type']
                        if (type(output_type) != safeJSON.SafeNoneClass):
                            g.add( (output_uri, dc.type, Literal(output_type,datatype=XSD.string )))
                        output_sectors = output['sector']
                        if (type(output_sectors) != safeJSON.SafeNoneClass):
                            output_sectors = output_sectors.replace("/ ", ", ")
                            output_sectors = output_sectors.replace(", ", "- ")
                            output_sectors = output_sectors.replace(",", ";")
                            output_sectors = output_sectors.replace("- ", ", ")
                            output_sectors_list = output_sectors.split(";")
                            for output_sector in output_sectors_list:
                                g.add( (output_uri, ukresearchproject.sector, Literal(output_sector,datatype=XSD.string )))
                        output_geographic_reach = output['geographicReach']
                        if (type(output_geographic_reach) != safeJSON.SafeNoneClass):
                            g.add( (output_uri, ukresearchproject.geographicReach, Literal(output_geographic_reach,datatype=XSD.string )))
                        output_year_first_provided = output['yearFirstProvided']
                        if (type(output_year_first_provided) != safeJSON.SafeNoneClass):
                            g.add( (output_uri, dc.available, Literal(output_year_first_provided,datatype=XSD.integer )))
                        output_stage = output['stage']
                        if (type(output_stage) != safeJSON.SafeNoneClass):
                            g.add( (output_uri, ukresearchproject.stage, Literal(output_stage,datatype=XSD.string )))
                        output_status = output['status']
                        if (type(output_status) != safeJSON.SafeNoneClass):
                            g.add( (output_uri, ukresearchproject.status, Literal(output_status,datatype=XSD.string )))
                        output_year_dev_completed = output['yearDevCompleted']
                        if (type(output_year_dev_completed) != safeJSON.SafeNoneClass):
                            g.add( (output_uri, frapo.hasCompletionDate, Literal(output_year_dev_completed,datatype=XSD.integer )))
                        if (output_class == 'ResearchMaterialOutput'):
                            if (output['providedToOthers']==True):
                                g.add( (output_uri, RDF.type, ukresearchproject.ProvidedToOthers ))
                        if (output_class == 'IntellectualPropertyOutput'):
                            if (output['licensed']=='Yes'):
                                g.add( (output_uri, RDF.type, ukresearchproject.Licensed ))
                            output_patent_id = output['patentId']
                            output_protection = output['protection']
                            output_year_protection_granted = output['yearProtectionGranted']
                            if((type(output_patent_id) != safeJSON.SafeNoneClass) or (type(output_protection) != safeJSON.SafeNoneClass) or (type(output_year_protection_granted) != safeJSON.SafeNoneClass)):
                                protection_uri_string = output_uri_string + '#protection'
                                protection_uri = URIRef(protection_uri_string)
                                g.add( (output_uri, ukresearchproject.hasProtection, protection_uri ))
                                g.add( (protection_uri, RDF.type, ukresearchproject.Protection ))
                                if(type(output_patent_id) != safeJSON.SafeNoneClass):
                                    g.add( (protection_uri, ukresearchproject.hasPatentId, Literal(output_patent_id,datatype=XSD.string ) ))
                                if(type(output_protection) != safeJSON.SafeNoneClass):
                                    g.add( (protection_uri, gr.category, Literal(output_protection,datatype=XSD.string ) ))
                                if(type(output_year_protection_granted) != safeJSON.SafeNoneClass):
                                    g.add( (protection_uri, ukresearchproject.yearProtectionGranted, Literal(output_year_protection_granted,datatype=XSD.integer ) ))
                        if (output_class == 'DisseminationOutput'):
                            output_results = output['results']
                            output_form = output['form']
                            output_primary_audience = output['primaryAudience']
                            output_year = output['year']
                            if (type(output_results) != safeJSON.SafeNoneClass):
                                g.add( (output_uri, ukresearchproject.results, Literal(output_results,datatype=XSD.string )))
                            if (type(output_form) != safeJSON.SafeNoneClass):
                                g.add( (output_uri, ukresearchproject.form, Literal(output_form,datatype=XSD.string )))
                            if (type(output_primary_audience) != safeJSON.SafeNoneClass):
                                g.add( (output_uri, dc.audience, Literal(output_primary_audience,datatype=XSD.string )))
                            if (type(output_year) != safeJSON.SafeNoneClass):
                                g.add( (output_uri, dc.date, Literal(output_year,datatype=XSD.integer )))
                        if (output_class == 'ImpactSummaryOutput'):
                            output_impact_types = output['impactType']
                            if (type(output_impact_types) != safeJSON.SafeNoneClass):
                                for output_impact_type_list in output_impact_types:
                                    output_impact_type_list = output_impact_type_list.split(",")
                                    for output_impact_type in output_impact_type_list:
                                        g.add( (output_uri, ukresearchproject.impactType, Literal(output_impact_type,datatype=XSD.string )))
                            output_first_year_of_impact = output['firstYearOfImpact']
                            if (type(output_first_year_of_impact) != safeJSON.SafeNoneClass):
                                g.add( (output_uri, ukresearchproject.firstYearOfImpact, Literal(output_first_year_of_impact,datatype=XSD.integer )))
                        if (output_class == 'SpinOutOutput'):
                            output_company_name = output['companyName']
                            if (type(output_company_name) != safeJSON.SafeNoneClass):
                                g.add( (output_uri, gr.legalName, Literal(output_company_name,datatype=XSD.string )))
                            output_year_company_formed = output['yearCompanyFormed']
                            if (type(output_year_company_formed) != safeJSON.SafeNoneClass):
                                g.add( (output_uri, ukresearchproject.yearFormed, Literal(output_year_company_formed,datatype=XSD.integer )))
                        if (output_class == 'CollaborationOutput'):
                            output_start = output['start']
                            if (type(output_start) != safeJSON.SafeNoneClass):
                                output_start = datetime.strptime(output_start,'%Y-%m-%d')
                                g.add( (output_uri, frapo.hasStartDate, Literal(output_start,datatype=XSD.dateTime) ))
                            output_end = output['end']
                            if (type(output_end) != safeJSON.SafeNoneClass):
                                output_end = datetime.strptime(output_end,'%Y-%m-%d')
                                g.add( (output_uri, frapo.hasEndDate, Literal(output_end,datatype=XSD.dateTime) ))
                            output_pi_contribution = output['piContribution']
                            if (type(output_pi_contribution) != safeJSON.SafeNoneClass):
                                g.add( (output_uri, ukresearchproject.piContribution, Literal(output_pi_contribution,datatype=XSD.string )))
                            output_partner_contribution = output['partnerContribution']
                            if (type(output_partner_contribution) != safeJSON.SafeNoneClass):
                                g.add( (output_uri, ukresearchproject.partnerContribution, Literal(output_partner_contribution,datatype=XSD.string )))
                            output_collaborator = output['collaboratingOrganisation']
                            if (type(output_collaborator) != safeJSON.SafeNoneClass):
                                for collab_org in collaborators:
                                    collab_org_name = collab_org['name']
                                    if (type(collab_org_name) != safeJSON.SafeNoneClass):
                                        if (collab_org_name == output_collaborator):
                                            collab_org_id = collab_org['id']
                                            if (type(collab_org_id) != safeJSON.SafeNoneClass):
                                                collab_org_uri_string = ahproject_base_uri + 'organisation/' + collab_org_id
                                                collab_org_uri = URIRef(collab_org_uri_string)
                                                g.add( (output_uri, vivo.hasCollaborator, collab_org_uri ))
                                g.add( (output_uri, vivo.hasCollaborator, Literal(output_collaborator,datatype=XSD.string )))
                            output_collaborator_country = output['country']
                            if (type(output_collaborator_country) != safeJSON.SafeNoneClass):
                                g.add( (output_uri, vcard.hasCountryName, Literal(output_collaborator_country,datatype=XSD.string) ))
                        if (output_class == 'FurtherFundingOutput'):
                            output_fund_uri_string = output_uri_string + '#fund'
                            output_fund_uri = URIRef(output_fund_uri_string)
                            g.add( (output_fund_uri, projectfunding.funds, output_uri ))
                            g.add( (output_fund_uri, RDF.type, projectfunding.Funding ))
                            output_funding_ref = output['fundingRef']
                            if (type(output_funding_ref) != safeJSON.SafeNoneClass):
                                g.add( (output_fund_uri, projectfunding.grantNumber, Literal(output_funding_ref,datatype=XSD.string) ))
                            output_start = output['start']
                            if (type(output_start) != safeJSON.SafeNoneClass):
                                output_start = datetime.strptime(output_start,'%Y-%m-%d')
                                g.add( (output_fund_uri, projectfunding.startDate, Literal(output_start,datatype=XSD.dateTime) ))
                            output_end = output['end']
                            if (type(output_end) != safeJSON.SafeNoneClass):
                                output_end = datetime.strptime(output_end,'%Y-%m-%d')
                                g.add( (output_fund_uri, projectfunding.endDate, Literal(output_end,datatype=XSD.dateTime) ))
                            output_amount = output['amountPounds']
                            if (type(output_amount) != safeJSON.SafeNoneClass):
                                g.add( (output_fund_uri, frapo.hasMonetaryValue, Literal(output_amount,datatype=XSD.decimal) ))
                                g.add( (output_fund_uri, frapo.hasCurrencyCode, currency_codes.GBP ))
                            output_original_country = output['currCountryCode']
                            output_original_language = output['currLang']
                            output_original_currency_code = output['currCode']
                            if ((type(output_original_country) != safeJSON.SafeNoneClass) or (type(output_original_language) != safeJSON.SafeNoneClass) or (type(output_original_currency_code) != safeJSON.SafeNoneClass)):
                                original_currency_uri_string = output_uri_string + '#originalCurrency'
                                original_currency_uri = URIRef(original_currency_uri_string)
                                g.add( (output_fund_uri, ukresearchproject.originalCurrency, original_currency_uri ))
                                g.add( (original_currency_uri, RDF.type, ukresearchproject.Currency ))
                                if (type(output_original_country) != safeJSON.SafeNoneClass):
                                    g.add( (original_currency_uri, frapo.hasCountryCode, Literal(output_original_country,datatype=XSD.string) ))
                                if (type(output_original_language) != safeJSON.SafeNoneClass):
                                    g.add( (original_currency_uri, frapo.hasLanguageCode, Literal(output_original_language,datatype=XSD.string) ))
                                if (type(output_original_currency_code) != safeJSON.SafeNoneClass):
                                    g.add( (original_currency_uri, frapo.hasCurrencyCode, Literal(output_original_currency_code,datatype=XSD.string) ))
                            output_funder_name = output['fundingOrg']
                            if (type(output_funder_name) != safeJSON.SafeNoneClass):
                                output_funder_uri_string = output_uri_string + '#funder'
                                output_funder_uri = URIRef(output_funder_uri_string)
                                g.add( (output_funder_uri, projectfunding.provides, output_fund_uri ))
                                g.add( (output_funder_uri, RDF.type, projectfunding.FundingBody ))
                                g.add( (output_funder_uri, vcard.hasOrganizationName, Literal(output_funder_name,datatype=XSD.string) ))
                                output_funder_country = output['country']
                                if (type(output_funder_country) != safeJSON.SafeNoneClass):
                                    g.add( (output_funder_uri, vcard.hasCountryName, Literal(output_funder_country,datatype=XSD.string) ))
                                if (type(output_funder_name) == funder_name):
                                    g.add( (funder, projectfunding.provides, output_fund_uri ))

#Related Projects
        project_hierarchy = data['projectOverview']['projectComposition']['project']['projectHierarchy']
        if (type(project_hierarchy) != safeJSON.SafeNoneClass):
            parents = project_hierarchy['parent']
            if (type(parents) != safeJSON.SafeNoneClass):
                for parent in parents:
                    parent_id = parent['id']
                    if (type(parent_id) != safeJSON.SafeNoneClass):
                        parent_uri_string = ahproject_base_uri + 'project/' + parent_id
                        parent_uri = URIRef(parent_uri_string)
                        children = parent['child']
                        if (type(children) != safeJSON.SafeNoneClass):
                            for child in children:
                                child_id = child['id']
                                if (type(child_id) != safeJSON.SafeNoneClass):
                                    child_uri_string = ahproject_base_uri + 'project/' + child_id
                                    child_uri = URIRef(child_uri_string)
                                    g.add( (parent_uri, ukresearchproject.isContinuedBy, child_uri ))
                                    g.add( (child_uri, ukresearchproject.continues, parent_uri ))
                                    grandchildren = child['child']
                                    if (type(grandchildren) != safeJSON.SafeNoneClass):
                                        for grandchild in grandchildren:
                                            grandchild_id = grandchild['id']
                                            if (type(grandchild_id) != safeJSON.SafeNoneClass):
                                                grandchild_uri_string = ahproject_base_uri + 'project/' + grandchild_id
                                                grandchild_uri = URIRef(grandchild_uri_string)
                                                g.add( (child_uri, ukresearchproject.isContinuedBy, grandchild_uri ))
                                                g.add( (grandchild_uri, ukresearchproject.continues, child_uri ))
                    

# Iterate over triples in store and print them out.
# print("--- printing raw triples ---")
#for s, p, o in g:
    #print((s, p, o))

# Write the output to a Turtle file:

    #turtle_file = 'turtle_files/file' + x + '.ttl'
    
file = open('AHRCDataToRDF_V9_20170120.ttl', "w+b")

file.write(g.serialize(format='turtle'))

file.close()

#print(g.serialize(format='turtle'))