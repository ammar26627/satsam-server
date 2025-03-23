import threading, uuid, os, sys, queue, torch
from datetime import timedelta
from timer_dict import TimerDict

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')

sys.path.append(os.path.join(ROOT_DIR, 'segment-anything'))
from segment_anything import sam_model_registry, SamPredictor

class QueueManager:
    def  __init__(self):
        self.request_queue = queue.Queue()
        self.job_results = TimerDict(timedelta(minutes=5))
        self.lock = threading.Lock()
        self.worker_running = False
        
        SAM_CHECKPOINT = os.path.join(ASSETS_DIR, "sam_vit_h_4b8939.pth")
        MODEL_TYPE = "vit_h"
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Model loaded successfully! Using device: {device}")

        sam = sam_model_registry[MODEL_TYPE](checkpoint=SAM_CHECKPOINT).to(device)
        self.predictor = SamPredictor(sam)

    def add_request_to_queue(self, request_data):
        job_id = str(uuid.uuid4())

        self.request_queue.put((job_id, request_data))
        queue_size = self.request_queue.qsize()
        estimated_time = queue_size * 5000

        if not self.worker_running:
            print('Worker Running')
            self.worker_running = True
            worker_thread = threading.Thread(target=self.process_results, daemon=True)
            worker_thread.start()

        return job_id, estimated_time
    
    def process_results(self):
        while not self.request_queue.empty():
            print('Generating Embeddings')
            job_id, image_array = self.request_queue.get()

            with self.lock:
                self.predictor.set_image(image_array)
                with torch.no_grad():
                    embeddings = self.predictor.get_image_embedding()

                embeddings_list = embeddings.cpu().numpy().reshape(-1).tolist()
                result = {
                    'message': 'Embeddings generated',
                    'embeddings': embeddings_list,
                    'shape': embeddings.shape
                }
                self.job_results[job_id] = result
                print(f'Embeddings Generated for ID {job_id}')

            self.request_queue.task_done()

        
        self.worker_running = False
