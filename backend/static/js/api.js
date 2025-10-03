/**
 * Cornerstone API Client
 * JavaScript functions to interact with Flask backend
 */

const API_BASE_URL = '/api';

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('API Error:', error);
        return { status: 'error', error_message: error.message };
    }
}

// ============================================================================
// DEMAND ANALYSIS
// ============================================================================

async function analyzeDemand(category = '') {
    return await apiRequest('/analyze-demand', 'POST', { category });
}

async function getRecommendations(minScore = 7.0) {
    return await apiRequest(`/recommendations?min_score=${minScore}`, 'GET');
}

async function getForecast(productId, timeframe = '30_days') {
    return await apiRequest('/forecast', 'POST', { product_id: productId, timeframe });
}

// ============================================================================
// BID COORDINATION
// ============================================================================

async function createBidWindow(jobId, productName, requiredQty, requiredSkill, durationHours = 96) {
    return await apiRequest('/create-bid', 'POST', {
        job_id: jobId,
        product_name: productName,
        required_qty: requiredQty,
        required_skill: requiredSkill,
        duration_hours: durationHours
    });
}

async function getBidStatus(jobId) {
    return await apiRequest(`/bid-status/${jobId}`, 'GET');
}

async function closeBidWindow(jobId) {
    return await apiRequest('/close-bid', 'POST', { job_id: jobId });
}

async function notifyWinners(jobId, winningMakerIds) {
    return await apiRequest('/notify-winners', 'POST', {
        job_id: jobId,
        winning_maker_ids: winningMakerIds
    });
}

// ============================================================================
// BID OPTIMIZATION
// ============================================================================

async function optimizeBids(jobId, requiredQty, requiredSkill) {
    return await apiRequest('/optimize-bids', 'POST', {
        job_id: jobId,
        required_qty: requiredQty,
        required_skill: requiredSkill
    });
}

async function getJobDetails() {
    return await apiRequest('/job-details', 'GET');
}

async function listManufacturers(skill = '') {
    return await apiRequest(`/manufacturers?skill=${skill}`, 'GET');
}

// ============================================================================
// TIMELINE MANAGEMENT
// ============================================================================

async function updateTimeline(makerId, newCompletionDate, reason = '') {
    return await apiRequest('/update-timeline', 'POST', {
        maker_id: makerId,
        new_completion_date: newCompletionDate,
        reason: reason
    });
}

async function getTimelineStatus(makerId = '') {
    return await apiRequest(`/timeline-status?maker_id=${makerId}`, 'GET');
}

async function sendMessageToManufacturer(makerId, message) {
    return await apiRequest('/send-message', 'POST', {
        maker_id: makerId,
        message: message
    });
}

// ============================================================================
// LOGISTICS
// ============================================================================

async function planLogistics(jobId, winningMakers) {
    return await apiRequest('/plan-logistics', 'POST', {
        job_id: jobId,
        winning_makers: winningMakers
    });
}

async function optimizeShipping(jobId) {
    return await apiRequest('/optimize-shipping', 'POST', { job_id: jobId });
}

async function trackShipments(jobId) {
    return await apiRequest(`/track-shipments/${jobId}`, 'GET');
}

async function coordinateConsolidation(jobId) {
    return await apiRequest('/coordinate-consolidation', 'POST', { job_id: jobId });
}

// ============================================================================
// ORCHESTRATED WORKFLOWS
// ============================================================================

async function executeCompleteWorkflowFlask() {
    /**
     * Execute workflow using Flask orchestration
     * Flask calls each agent tool sequentially
     */
    return await apiRequest('/complete-workflow-flask', 'POST', {});
}

async function executeCompleteWorkflowADK() {
    /**
     * Execute workflow using ADK SequentialAgent
     * Master Orchestrator coordinates all 5 agents autonomously
     */
    return await apiRequest('/complete-workflow-adk', 'POST', {});
}

// ============================================================================
// HELPER FUNCTIONS FOR UI
// ============================================================================

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="flex items-center justify-center p-4"><div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div></div>';
    }
}

function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">${message}</div>`;
    }
}

function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<div class="bg-green-50 border border-green-200 rounded-lg p-4 text-green-800">${message}</div>`;
    }
}
