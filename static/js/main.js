// Globalt JavaScript for nettsiden

// API-hjelper for datalagrting
const StorageAPI = {
    // Hent brukerdata
    async getData(key = null) {
        try {
            const url = key ? `/api/data/${key}` : '/api/data';
            const response = await fetch(url);
            if (!response.ok) {
                if (response.status === 401) {
                    console.log('Ikke innlogget');
                    return null;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching data:', error);
            return null;
        }
    },

    // Lagre en datanøkkel
    async setData(key, value) {
        try {
            const response = await fetch(`/api/data/${key}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ value: value })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error saving data:', error);
            return null;
        }
    },

    // Sett flere datanøkler
    async setDataBulk(data) {
        try {
            const response = await fetch('/api/data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error saving bulk data:', error);
            return null;
        }
    },

    // Slett en datanøkkel
    async deleteData(key) {
        try {
            const response = await fetch(`/api/data/${key}`, {
                method: 'DELETE'
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error deleting data:', error);
            return null;
        }
    }
};

// Eksempel på bruk:
// StorageAPI.setData('telefon', '12345678')
// StorageAPI.getData('telefon')
// StorageAPI.getData() - hent all data
// StorageAPI.deleteData('telefon')
