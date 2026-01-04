// src/services/api.js
const API_BASE_URL = 'http://localhost:8000';

class APIService {
  // Helper method for API calls
  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'API request failed');
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  // Stats & Dashboard
  async getStats() {
    return this.request('/api/stats');
  }

  async getPlatformStats() {
    return this.request('/api/statistics');
  }

  // Blueprints
  async getBlueprints() {
    return this.request('/api/blueprints');
  }

  async getBlueprint(blueprintId) {
    return this.request(`/api/blueprints/${blueprintId}`);
  }

  // Campaigns
  async createCampaign(userId, difficulty, count = null) {
    return this.request('/api/campaigns', {
      method: 'POST',
      body: JSON.stringify({
        user_id: userId,
        difficulty: difficulty,
        count: count
      }),
    });
  }

  async getCampaignProgress(campaignId, userId) {
    return this.request(`/api/campaigns/${campaignId}/progress?user_id=${userId}`);
  }

  // Machines
  async getMachines() {
    return this.request('/api/machines');
  }

  async getMachine(machineId) {
    return this.request(`/api/machines/${machineId}`);
  }

  async getMachineStats(machineId) {
    return this.request(`/api/machines/${machineId}/stats`);
  }

  // Flags
  async validateFlag(machineId, flag, userId) {
    return this.request('/api/flags/validate', {
      method: 'POST',
      body: JSON.stringify({
        machine_id: machineId,
        flag: flag,
        user_id: userId
      }),
    });
  }

  // Docker Management
  async startContainers() {
    return this.request('/api/docker/start', {
      method: 'POST',
    });
  }

  async stopContainers() {
    return this.request('/api/docker/stop', {
      method: 'POST',
    });
  }

  async restartContainers() {
    return this.request('/api/docker/restart', {
      method: 'POST',
    });
  }

  async destroyContainers() {
    return this.request('/api/docker/destroy', {
      method: 'DELETE',
    });
  }

  async getDockerStatus() {
    return this.request('/api/docker/status');
  }

  // Users
  async createUser(username, email, role = 'student') {
    return this.request('/api/users', {
      method: 'POST',
      body: JSON.stringify({
        username: username,
        email: email,
        role: role
      }),
    });
  }

  async getUser(userId) {
    return this.request(`/api/users/${userId}`);
  }

  async getUserProgress(userId) {
    return this.request(`/api/users/${userId}/progress`);
  }

  // Leaderboard
  async getLeaderboard(limit = 100, timeframe = 'all_time') {
    return this.request(`/api/leaderboard?limit=${limit}&timeframe=${timeframe}`);
  }

  // Health Check
  async healthCheck() {
    return this.request('/health');
  }
}

export default new APIService();
