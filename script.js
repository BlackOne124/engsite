class CareerCosmos {
    constructor() {
        this.userData = null;
        this.currentSection = 'dashboard';
        this.aiState = null;
        this.aiAnswers = {};
        this.init();
    }

    async init() {
        try {
            await this.loadUserData();
            this.setupEventListeners();
            this.updateUI();
            this.setupAnimations();
            this.showNotification('Career Cosmos initialized! Ready for launch!');
        } catch (error) {
            console.error('Error initializing Career Cosmos:', error);
        }
    }

    async loadUserData() {
        try {
            const response = await fetch('/api/user');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.userData = await response.json();
        } catch (error) {
            console.error('Error loading cosmic data:', error);
            // Fallback data
            this.userData = {
                level: 1,
                xp: 0,
                coins: 0,
                badges: [],
                completed_quests: [],
                career_path: null,
                skills_progress: {
                    'Python': 65,
                    'SQL': 40,
                    'Machine Learning': 25,
                    'Communication': 70,
                    'Project Management': 35
                },
                selected_goals: [],
                completed_goals: [],
                daily_streak: 1,
                total_quests_completed: 0,
                total_xp_earned: 0,
                total_coins_earned: 0,
                last_login: new Date().toISOString()
            };
            this.showNotification('Using offline mode - some features limited');
        }
    }

    setupEventListeners() {
        // Navigation stars - безопасное добавление обработчиков
        const navStars = document.querySelectorAll('.nav-star');
        if (navStars.length > 0) {
            navStars.forEach(star => {
                star.addEventListener('click', (e) => {
                    const section = e.currentTarget.getAttribute('data-section');
                    this.navigateToSection(section);
                });
            });
        }

        // AI Chat - проверка существования элементов
        const sendButton = document.getElementById('send-ai-message');
        const chatInput = document.getElementById('ai-chat-input');
        
        if (sendButton && chatInput) {
            sendButton.addEventListener('click', () => this.sendAIMessage());
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.sendAIMessage();
            });
        }

        // Quick questions
        const quickQuestions = document.querySelectorAll('.quick-question');
        if (quickQuestions.length > 0) {
            quickQuestions.forEach(button => {
                button.addEventListener('click', (e) => {
                    const question = e.target.getAttribute('data-question');
                    if (chatInput) {
                        chatInput.value = question;
                        this.sendAIMessage();
                    }
                });
            });
        }

        // Cosmic background interactions
        document.addEventListener('mousemove', this.handleMouseMove.bind(this));
    }

    navigateToSection(section) {
        // Update active navigation
        document.querySelectorAll('.nav-star').forEach(star => {
            star.classList.remove('active');
        });
        
        const activeNav = document.querySelector(`[data-section="${section}"]`);
        if (activeNav) {
            activeNav.classList.add('active');
        }

        // Update active section
        document.querySelectorAll('.cosmic-section').forEach(sectionEl => {
            sectionEl.classList.remove('active');
        });
        
        const targetSection = document.getElementById(section);
        if (targetSection) {
            targetSection.classList.add('active');
        }

        // Update page title
        const titles = {
            'dashboard': 'Mission Control',
            'profile': 'Astronaut Profile',
            'galaxy': 'Career Galaxy',
            'quests': 'Space Missions',
            'goals': 'Stellar Goals',
            'ai': 'AI Navigator',
            'achievements': 'Cosmic Badges'
        };
        
        const pageTitle = document.getElementById('page-title');
        if (pageTitle) {
            pageTitle.textContent = titles[section] || 'Career Cosmos';
        }

        this.currentSection = section;
        this.loadSectionData(section);
    }

    // Обновите метод updateSkills для корректного расчета progress ring
    updateSkills() {
        const skillsUniverse = document.getElementById('skills-universe');
        if (!skillsUniverse || !this.userData.skills_progress) return;

        let skillsHTML = '';
        for (const [skill, progress] of Object.entries(this.userData.skills_progress)) {
            const circumference = 2 * Math.PI * 25; // для радиуса 25
            const offset = circumference - (progress / 100) * circumference;
            
            skillsHTML += `
                <div class="skill-planet">
                    <div class="planet-progress">
                        <div class="progress-ring small">
                            <svg width="60" height="60">
                                <circle class="ring-back" cx="30" cy="30" r="25" stroke-width="3"></circle>
                                <circle class="ring-front" cx="30" cy="30" r="25" stroke-width="3" 
                                        style="stroke-dasharray: ${circumference}; stroke-dashoffset: ${offset}"></circle>
                            </svg>
                        </div>
                        <div class="skill-name">${skill}</div>
                    </div>
                    <div class="skill-percent">${progress}%</div>
                </div>
            `;
        }
        skillsUniverse.innerHTML = skillsHTML;
    }

    // Добавьте обработку ошибок в AI чат
    async sendAIMessage() {
        const input = document.getElementById('ai-chat-input');
        const message = input?.value.trim();

        if (!message) return;

        this.addAIMessage(message, 'user');
        if (input) input.value = '';

        try {
            const response = await fetch('/api/ai_chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const data = await response.json();

            if (data.type === 'question') {
                this.addAIQuestion(data.text, data.options);
            } else if (data.type === 'final_plan') {
                this.addAIFinalPlan(data.text);
                await this.loadUserData();
                this.updateUI();
            } else {
                this.addAIMessage(data.text, 'ai');
            }
        } catch (error) {
            console.error('Error sending AI message:', error);
            this.addAIMessage('🚨 Cosmic communication disrupted! Mission control is experiencing technical difficulties. Please try again later.', 'ai');
        }
    }

    // Обновите метод completeQuest для обработки ошибок
    async completeQuest(questId) {
        try {
            const response = await fetch('/api/complete_quest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ quest_id: questId })
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            const result = await response.json();
            if (result.success) {
                this.userData = result.user_data;
                this.updateUI();
                this.showNotification('🎉 Mission accomplished! Stellar rewards received!');

                // Refresh current section if it's quests
                if (this.currentSection === 'quests') {
                    this.updateQuests();
                }
            }
        } catch (error) {
            console.error('Error completing mission:', error);
            this.showNotification('❌ Mission failed to transmit. Please check your connection.');
        }
    }

    // Добавьте метод для безопасного показа уведомлений
    showNotification(message) {
        try {
            const notification = document.getElementById('notification');
            const messageEl = notification?.querySelector('.notification-message');

            if (notification && messageEl) {
                messageEl.textContent = message;
                notification.classList.add('show');

                setTimeout(() => {
                    notification.classList.remove('show');
                }, 4000);
            } else {
                // Fallback: использовать alert если уведомление не найдено
                alert(message);
            }
        } catch (error) {
            console.error('Error showing notification:', error);
            alert(message); // Fallback
        }
    }
}

// Безопасная инициализация
document.addEventListener('DOMContentLoaded', () => {
    try {
        new CareerCosmos();
    } catch (error) {
        console.error('Failed to initialize Career Cosmos:', error);
        alert('Career Cosmos failed to launch. Please refresh the page.');
    }
});
