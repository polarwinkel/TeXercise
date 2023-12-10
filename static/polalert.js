const version = 'v1.2.0';
class Polalert {
    constructor() {
        this.bgBox = document.createElement('div');
        this.bgBox.setAttribute('id', 'polalertBg');
        this.bgBox.style.display = 'none';
        this.bgBox.style.position = 'fixed';
        this.bgBox.style.z_index = '1';
        this.bgBox.style.left = '0';
        this.bgBox.style.top = '0';
        this.bgBox.style.height = '100%';
        this.bgBox.style.width = '100%';
        this.bgBox.style.overflow = 'auto'; // Enable scroll
        this.bgBox.style.background = 'rgba(0,0,0,0.5)';
        this.box = document.createElement('div');
        this.box.parent = this.bgBox;
        this.box.setAttribute('id', 'polalert');
        this.box.style.display = 'block';
        this.box.style.minHeight = '12em';
        this.box.style.width = '50%';
        this.box.style.minWidth = '18em';
        this.box.style.maxWidth = '100%';
        this.box.style.backdropFilter = 'blur(0.3em)';
        this.box.style.boxShadow = '0.6em 0.6em 0.3em rgba(0,0,0,0.5)';
        this.box.style.borderRadius = '0.6em';
        if (window.innerWidth > 981) {
            this.box.style.marginLeft = '25%';
        } else {
            this.box.style.width = '80%';
            this.box.style.marginLeft = '5%';
        }
        this.box.style.marginTop = '6em';
        this.box.style.padding = '1.2em';
        this.box.style.textAlign = 'center';
        this.box.style.fontSize = '1.2em';
        this.bgBox.appendChild(this.box);
        this.buttonOk = document.createElement('button');
        this.buttonOk.parent = this.box;
        this.buttonOk.setAttribute('id', 'polalertOk');
        this.buttonOk.style.width = '12em';
        this.buttonOk.style.backgroundColor = 'rgba(0, 255, 0, 0.7)';
        this.buttonOk.style.border = '0.1em solid gray';
        this.buttonOk.style.borderRadius = '0.6em';
        this.buttonOk.style.fontSize = '1.4em';
        this.buttonOk.innerHTML = '<p>&#10003;</p>';
        this.buttonNo = document.createElement('button');
        this.buttonNo.parent = this.box;
        this.buttonNo.setAttribute('id', 'polalertNo');
        this.buttonNo.style.width = '12em';
        this.buttonNo.style.backgroundColor = 'rgba(255, 0, 0, 0.7)';
        this.buttonNo.style.border = '0.1em solid gray';
        this.buttonNo.style.borderRadius = '0.6em';
        this.buttonNo.style.fontSize = '1.4em';
        this.buttonNo.innerHTML = '<p>&#10005;</p>';
    }
    next() {
    }
    hello() {
        this.box.style.backgroundColor = 'rgba(200, 200, 200, 0.8)';
        this.box.innerHTML = '<p>Hello World!</p>';
        this.box.appendChild(this.buttonOk);
        document.body.appendChild(this.bgBox);
        this.buttonOk.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
        };
        this.bgBox.style.display = 'block';
        document.getElementById('polalertOk').focus();
    }
    message(msg) {
        this.box.style.backgroundColor = 'rgba(255, 255, 255, 0.7)';
        this.box.style.backdropFilter = 'blur(0.3em)';
        this.box.innerHTML = '<p>'+msg+'</p>';
        this.box.appendChild(this.buttonOk);
        document.body.appendChild(this.bgBox);
        this.buttonOk.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
        };
        this.bgBox.style.display = 'block';
        document.getElementById('polalertOk').focus();
    }
    warning(warn) {
        this.box.style.backgroundColor = 'rgba(255, 180, 0, 0.7)';
        this.box.style.backdropFilter = 'blur(0.3em)';
        this.box.innerHTML = '<p>'+warn+'</p>';
        this.box.appendChild(this.buttonOk);
        document.body.appendChild(this.bgBox);
        this.buttonOk.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
        };
        this.bgBox.style.display = 'block';
        document.getElementById('polalertOk').focus();
    }
    error(err) {
        this.box.style.backgroundColor = 'rgba(255, 50, 50, 0.7)';
        this.box.style.backdropFilter = 'blur(0.3em)';
        this.box.innerHTML = '<p>'+err+'</p>';
        this.box.appendChild(this.buttonOk);
        document.body.appendChild(this.bgBox);
        this.buttonOk.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
        };
        this.bgBox.style.display = 'block';
        document.getElementById('polalertOk').focus();
    }
    boolean(msg, str='') {
        this.box.style.backgroundColor = 'rgba(200, 200, 200, 0.8)';
        this.answer = null;
        this.box.innerHTML = '<p>'+msg+'</p>';
        this.box.appendChild(this.buttonOk);
        this.buttonOk.style.margin = '0.3em';
        this.buttonOk.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
            paOk(str);
        };
        this.box.appendChild(this.buttonNo);
        this.buttonNo.style.margin = '0.3em';
        this.buttonNo.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
            paNo(str);
        };
        document.body.appendChild(this.bgBox);
        this.bgBox.style.display = 'block';
        document.getElementById('polalertNo').focus();
        return[this.buttonOk, this.buttonNo];
    }
    input(msg, password=false) {
        this.box.style.backgroundColor = 'rgba(200, 200, 200, 0.8)';
        this.answer = null;
        this.box.innerHTML = '<p>'+msg+'</p>';
        if (password) this.box.innerHTML += '<input type="password" id="paInput" style="max-width:100%"></input><br />'
        else this.box.innerHTML += '<input type="text" id="paInput" style="max-width:100%"></input><br />';
        this.box.appendChild(this.buttonOk);
        this.buttonOk.style.margin = '0.3em';
        this.buttonOk.onclick = function () {
            var inputtext = document.getElementById('paInput').value
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
            paInputReceive(inputtext);
        };
        this.box.appendChild(this.buttonNo);
        this.buttonNo.style.margin = '0.3em';
        this.buttonNo.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
            paInputReceive(false);
        };
        document.body.appendChild(this.bgBox);
        this.bgBox.style.display = 'block';
        document.getElementById('paInput').focus();
        return[this.buttonOk, this.buttonNo];
    }
}
var pa = new Polalert();
