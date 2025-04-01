FROM condaforge/miniforge3:latest

ENV DEBIAN_FRONTEND=noninteractive


# Pre-warm the model, by downloading it into cache. Pinning transformers/pytorch to be sure...
# TODO: Would be nice to find a way to pre-warm without any dependencies at all, e.g. by downloading with the default pip and then moving it to the mamba env cache.
COPY environment.yml /
RUN mamba env create --quiet --file /environment.yml
RUN mamba run --live-stream -n llm pip3 install transformers==4.50.3 torch==2.6.0+cpu --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple
ARG MODEL_NAME=medalpaca/medalpaca-7b
ENV MODEL_NAME=$MODEL_NAME
COPY pre-warm.py /
RUN mamba run --live-stream -n llm python3 -m pre-warm.py $MODEL_NAME


# Install appropriate CUDA version
ARG CUDA_MAJOR
ARG CUDA_MINOR
RUN apt-get update && apt-get install -y build-essential libxml2
RUN wget https://raw.githubusercontent.com/TimDettmers/bitsandbytes/main/install_cuda.sh
RUN bash install_cuda.sh $CUDA_MAJOR$CUDA_MINOR /cuda 1
RUN ln -s /cuda/cuda-$CUDA_MAJOR.$CUDA_MINOR/targets/x86_64-linux/lib/libcudart.so /opt/conda/lib/libcudart.so
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/
RUN echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/' >> ~/.bashrc


# Install the environment and requirements
COPY requirements.txt /
RUN mamba run --live-stream -n llm pip3 uninstall -y transformers torch
RUN mamba run --live-stream -n llm pip3 install -r /requirements.txt
RUN mamba run --live-stream -n llm pip3 install torch --index-url https://download.pytorch.org/whl/cu$CUDA_MAJOR$CUDA_MINOR
RUN mamba install -y -n llm -c conda-forge libstdcxx-ng=13
RUN mamba install -y -n llm -c conda-forge gcc=13
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
RUN mamba clean --all -y


# Copy over source
COPY app /app

# Run the server
CMD [ "mamba", "run", "--live-stream", "-n", "llm", "flask", "--app", "app", "run", "--host", "0.0.0.0"]