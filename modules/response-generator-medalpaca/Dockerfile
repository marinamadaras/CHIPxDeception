FROM condaforge/miniforge3:latest


ARG CUDA_MAJOR
ARG CUDA_MINOR
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y build-essential libxml2
RUN wget https://raw.githubusercontent.com/TimDettmers/bitsandbytes/main/install_cuda.sh
RUN bash install_cuda.sh $CUDA_MAJOR$CUDA_MINOR /cuda 1
RUN ln -s /cuda/cuda-$CUDA_MAJOR.$CUDA_MINOR/targets/x86_64-linux/lib/libcudart.so /opt/conda/lib/libcudart.so
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/
RUN echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/' >> ~/.bashrc

COPY requirements.txt /
COPY environment.yml /
RUN mamba env create --quiet --file /environment.yml
RUN mamba run -n medalpaca pip3 install torch --index-url https://download.pytorch.org/whl/cu$CUDA_MAJOR$CUDA_MINOR
RUN mamba install -y -n medalpaca -c conda-forge libstdcxx-ng=13
RUN mamba install -y -n medalpaca -c conda-forge gcc=13
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
RUN mamba clean --all -y

# RUN mamba run -n medalpaca python3 -m bitsandbytes
# CMD ["conda", "run", "-n", "my_env", "python", "app.py"]

# RUN echo '. "/opt/conda/etc/profile.d/conda.sh"' >> $SINGULARITY_ENVIRONMENT
# RUN echo 'conda activate medalpaca' >> $SINGULARITY_ENVIRONMENT


# RUN git clone https://github.com/timdettmers/bitsandbytes.git
# RUN cd bitsandbytes

# RUN CUDA_VERSION=126 make cuda12x
# RUN python setup.py install
# RUN ln -s /usr/lib/wsl/lib/libcuda.so [path to your env here]/lib/libcuda.so
# COPY requirements.txt /
# RUN pip3 install -r /requirements.txt
# RUN apt-get update && apt-get install -y curl \
# libzmq3-dev \
# build-essential \
# g++ \
# libsm6 \
# libxext6 \
# libxrender-dev \
# libgl1




# CMD ["sleep", "infinity"]

# This "pre-warms" the model, by downloading it onto the cache
RUN mamba run -n medalpaca python3 -c "from transformers import pipeline; pl = pipeline(\"text-generation\", model=\"medalpaca/medalpaca-7b\", tokenizer=\"medalpaca/medalpaca-7b\", device=-1);"

# Copy over source
COPY app /app

# Run the server
CMD [ "mamba", "run", "--live-stream", "-n", "medalpaca", "flask", "--app", "app", "run", "--host", "0.0.0.0"]