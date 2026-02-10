// dashboard_vision.js
class Node {
    constructor(type, text) {
        this.type = type;
        this.text = text;
        this.element = document.createElement('div');
        this.element.classList.add('node');
        this.element.innerHTML = text;
        this.element.style.backgroundColor = this.getTypeColor();
    }

    getTypeColor() {
        switch (this.type) {
            case 'understanding':
                return '#6366f1';
            case 'worker':
                return '#8b5cf6';
            case 'helper':
                return '#06b6d4';
            case 'expert':
                return '#f59e0b';
            default:
                return '#fff';
        }
    }

    addRainbowBorder() {
        this.element.classList.add('rainbow-border');
    }

    removeRainbowBorder() {
        this.element.classList.remove('rainbow-border');
    }
}

class Dashboard {
    constructor() {
        this.nodes = [];
        this.mainCanvas = document.querySelector('.main-canvas');
    }

    addNode(node) {
        this.nodes.push(node);
        this.mainCanvas.appendChild(node.element);
    }

    removeNode(node) {
        const index = this.nodes.indexOf(node);
        if (index !== -1) {
            this.nodes.splice(index, 1);
            node.element.remove();
        }
    }

    animateNodes() {
        this.nodes.forEach((node, index) => {
            node.addRainbowBorder();
            setTimeout(() => {
                node.removeRainbowBorder();
            }, 3000);
        });
    }

    thunkThunkThunkCollapse() {
        this.nodes.reverse();
        this.nodes.forEach((node, index) => {
            setTimeout(() => {
                node.element.style.transform = 'scale(0)';
                node.element.style.opacity = 0;
                setTimeout(() => {
                    this.removeNode(node);
                }, 250);
            }, index * 250 + 120);
        });
    }
}

const dashboard = new Dashboard();

// Test nodes
const node1 = new Node('understanding', 'Node 1');
const node2 = new Node('worker', 'Node 2');
const node3 = new Node('helper', 'Node 3');

dashboard.addNode(node1);
dashboard.addNode(node2);
dashboard.addNode(node3);

// Animate nodes
dashboard.animateNodes();

// Thunk-thunk-thunk collapse
setTimeout(() => {
    dashboard.thunkThunkThunkCollapse();
}, 5000);