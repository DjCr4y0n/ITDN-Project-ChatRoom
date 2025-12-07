// javascript
// client-side chat logic — saved as static/chat.js (must not contain HTML <script> tags)
document.addEventListener('DOMContentLoaded', () => {
  // connect (default will send cookies so Flask session is available)
  const socket = typeof io === 'function' ? io() : null;

  if (!socket) {
    console.error('Socket.IO client not found. Ensure socket.io client is loaded before static/chat.js');
    return;
  }

  const chatbox = document.getElementById('chatbox');
  const input = document.getElementById('msgInput');
  const btn = document.getElementById('sendBtn');

  // debug helpers
  socket.on('connect', () => console.log('socket connected, id=', socket.id));
  socket.on('connect_error', (err) => console.error('connect_error', err));
  socket.on('disconnect', (reason) => console.log('socket disconnected:', reason));

  // receive messages
  socket.on('chat_message', (data) => {
    if (!chatbox) return;
    const el = document.createElement('div');
    el.className = 'message';
    el.textContent = `${data.username}: ${data.message}`;
    chatbox.appendChild(el);
    chatbox.scrollTop = chatbox.scrollHeight;
  });

  function send() {
    if (!input) return;
    const msg = input.value.trim();
    if (!msg) return;
    socket.emit('chat_message', { message: msg });
    input.value = '';
  }

  if (btn) btn.addEventListener('click', send);
  if (input) input.addEventListener('keydown', (e) => { if (e.key === 'Enter') send(); });
});
