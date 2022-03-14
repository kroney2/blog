const navbarTemplate = document.createElement('template');
navbarTemplate.innerHTML = `
<style>
    .navbar{
        text-align: center;
    }
    .navbar a{
        color: black;
    }
</style>

<div class="navbar">
    <ul>
        <a href="file:////home/caleb/src/kmg-site/index.html">home</a>
        <a href="file:////home/caleb/src/kmg-site/posts.html">posts</a>
    </ul>
</div>
`

class Navbar extends HTMLElement {
    constructor() { super(); }

    connectedCallback() {
        const shadowRoot = this.attachShadow({ mode: 'open' });
        shadowRoot.appendChild(navbarTemplate.content);
    }
}

customElements.define('navbar-component', Navbar);
