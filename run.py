import socket
import webbrowser
import threading
import time
import sys
import uvicorn

def find_available_port(preferred_port=8000, fallback_ports=[8080, 8001, 8050, 5000]):
    ports = [preferred_port] + [p for p in fallback_ports if p != preferred_port]
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    return preferred_port

def open_browser(port):
    time.sleep(1.2)
    webbrowser.open(f"http://127.0.0.1:{port}")

if __name__ == "__main__":
    # Check if custom port provided in args
    target_port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        target_port = int(sys.argv[1])
    else:
        target_port = find_available_port(preferred_port=8000)

    print("=================================================================")
    print(" 🚀 OmniLead AI & Cold Caller CRM Automation is Launching...")
    print(f" 🌐 Application URL: http://127.0.0.1:{target_port}")
    print(" 📍 Cascading Target: Country -> State -> City (e.g. Jalgaon)")
    print(" 💼 Services: Website Dev | ERP Software | Custom Software")
    print("=================================================================")
    
    threading.Thread(target=open_browser, args=(target_port,), daemon=True).start()
    uvicorn.run("backend.main:app", host="127.0.0.1", port=target_port, reload=True)
