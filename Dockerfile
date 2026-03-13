FROM python:3.12-slim-bookworm

LABEL bos.type="base-image"
LABEL bos.name="bospy"
LABEL bos.author="James"
LABEL bos.description="a base for building python apps and drivers"

COPY /bindings/python/bospy/src/ /opt/bos/bospy/src/
COPY /bindings/python/bospy/pyproject.toml /opt/bos/bospy/
COPY /bindings/python/bospy/README.md /opt/bos/bospy/
RUN pip install -e /opt/bos/bospy/

CMD ["python"]