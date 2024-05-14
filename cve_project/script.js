const cveTable = document.getElementById('cve-table');
const cveDataContainer = document.getElementById('cve-data');
const totalCountSpan = document.getElementById('total-count');
const loadingIndicator = document.createElement('p'); // New element for loading indicator

function updateTable(data, totalCount) {
    cveDataContainer.innerHTML = ''; // Clear previous content
    totalCountSpan.textContent = totalCount;

    data.forEach(cve => {
        const row = document.createElement('tr');

        const cveIdCell = document.createElement('td');
        cveIdCell.textContent = cve.cve_id;

        const identifierCell = document.createElement('td');
        identifierCell.textContent = cve.cve_data_meta ? .id || "-"; // Adjust based on API response structure

        const publishedDateCell = document.createElement('td');
        publishedDateCell.textContent = cve.publishedDate;

        const lastModifiedDateCell = document.createElement('td');
        lastModifiedDateCell.textContent = cve.lastModifiedDate;

        const statusCell = document.createElement('td');
        statusCell.textContent = cve.cve_data_meta ? .status || "-"; // Adjust based on API response structure

        row.appendChild(cveIdCell);
        row.appendChild(identifierCell);
        row.appendChild(publishedDateCell);
        row.appendChild(lastModifiedDateCell);
        row.appendChild(statusCell);

        cveDataContainer.appendChild(row);
    });
}

// Replace with the actual NVD API endpoint URL
const apiUrl = 'https://services.nvd.nist.gov/rest/json/cves/2.0';

function fetchData() {
    loadingIndicator.textContent = "Loading CVE data...";
    cveDataContainer.appendChild(loadingIndicator);

    fetch(apiUrl)
        .then(response => {
            loadingIndicator.remove(); // Remove loading indicator on success

            if (!response.ok) {
                throw new Error(`API request failed with status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Assuming "totalResults" gives the total count
            updateTable(data.results, data.totalResults);
        })
        .catch(error => {
            console.error('Error fetching CVEs:', error);

            // More informative error handling
            if (error.message.includes('404')) {
                cveDataContainer.innerHTML = '<p>API endpoint not found.</p>';
            } else if (error.message.includes('429')) {
                cveDataContainer.innerHTML = '<p>API rate limit exceeded. Please try again later.</p>';
            } else {
                cveDataContainer.innerHTML = '<p>Error retrieving CVE data.</p>';
            }
        });
}

fetchData();