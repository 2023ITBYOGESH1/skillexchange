// Main JavaScript for P2P

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        });
    }, 5000);

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        let debounceTimer;
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(function() {
                const query = searchInput.value;
                if (query.length >= 2) {
                    // Trigger search
                    const form = searchInput.closest('form');
                    if (form) form.submit();
                }
            }, 300);
        });
    }

    // Skill type toggle
    const skillTypeSelect = document.getElementById('skill_type');
    if (skillTypeSelect) {
        skillTypeSelect.addEventListener('change', function() {
            const offeredSection = document.getElementById('offered-section');
            const wantedSection = document.getElementById('wanted-section');
            
            if (this.value === 'offered') {
                if (offeredSection) offeredSection.style.display = 'block';
                if (wantedSection) wantedSection.style.display = 'none';
            } else if (this.value === 'wanted') {
                if (offeredSection) offeredSection.style.display = 'none';
                if (wantedSection) wantedSection.style.display = 'block';
            }
        });
    }

    // Bookmark toggle
    const bookmarkButtons = document.querySelectorAll('.bookmark-btn');
    bookmarkButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const skillId = this.dataset.skillId;
            const url = this.dataset.url;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.classList.toggle('bookmarked');
                    const icon = this.querySelector('i');
                    if (icon) {
                        icon.classList.toggle('far');
                        icon.classList.toggle('fas');
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Chat refresh
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
        const userId = chatMessages.dataset.userId;
        
        function loadMessages() {
            fetch(`/chat/api/messages/${userId}`)
                .then(response => response.json())
                .then(messages => {
                    messages.forEach(msg => {
                        const existingMsg = document.querySelector(`[data-message-id="${msg.id}"]`);
                        if (!existingMsg) {
                            const msgDiv = document.createElement('div');
                            msgDiv.className = `message ${msg.sender_id == userId ? 'received' : 'sent'}`;
                            msgDiv.dataset.messageId = msg.id;
                            msgDiv.innerHTML = `
                                ${msg.content}
                                <div class="message-time">${formatTime(msg.created_at)}</div>
                            `;
                            chatMessages.appendChild(msgDiv);
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                        }
                    });
                });
        }
        
        // Refresh every 5 seconds
        setInterval(loadMessages, 5000);
    }

    // Send message form
    const sendMessageForm = document.getElementById('send-message-form');
    if (sendMessageForm) {
        sendMessageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            fetch('/chat/api/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    receiver_id: formData.get('receiver_id'),
                    content: formData.get('content')
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.id) {
                    const messageInput = this.querySelector('input[name="content"]');
                    messageInput.value = '';
                    
                    // Add message to chat
                    const chatMessages = document.getElementById('chat-messages');
                    const msgDiv = document.createElement('div');
                    msgDiv.className = 'message sent';
                    msgDiv.dataset.messageId = data.id;
                    msgDiv.innerHTML = `
                        ${data.content}
                        <div class="message-time">${formatTime(data.created_at)}</div>
                    `;
                    chatMessages.appendChild(msgDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            });
        });
    }

    // Rating stars
    const ratingInputs = document.querySelectorAll('.rating-input');
    ratingInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const rating = this.value;
            const stars = this.closest('.rating-container').querySelectorAll('.star');
            stars.forEach(function(star, index) {
                if (index < rating) {
                    star.classList.add('filled');
                } else {
                    star.classList.remove('filled');
                }
            });
        });
    });

    // Confirm delete
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Tab switching
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(function(tab) {
        tab.addEventListener('click', function() {
            const target = this.dataset.target;
            
            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Show target content
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(c => c.style.display = 'none');
            document.getElementById(target).style.display = 'block';
        });
    });

    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    // Image preview
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('image-preview');
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Unread message count
    function updateUnreadCount() {
        fetch('/chat/api/unread')
            .then(response => response.json())
            .then(data => {
                const badge = document.querySelector('.unread-badge');
                if (badge) {
                    badge.textContent = data.unread;
                    badge.style.display = data.unread > 0 ? 'block' : 'none';
                }
            });
    }
    
    // Update every 30 seconds
    if (document.querySelector('.chat-link')) {
        setInterval(updateUnreadCount, 30000);
    }
});

// Helper functions
function formatTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return Math.floor(diff / 60000) + 'm ago';
    if (diff < 86400000) return Math.floor(diff / 3600000) + 'h ago';
    
    return date.toLocaleDateString();
}

function showNotification(message, type = 'info') {
    const container = document.querySelector('.flash-messages');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    container.appendChild(alert);
    
    setTimeout(function() {
        alert.style.opacity = '0';
        setTimeout(function() {
            alert.remove();
        }, 500);
    }, 5000);
}

