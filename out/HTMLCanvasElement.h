#pragma once

#include "em_import.h"

EM_IMPORT_STRUCT("HTMLCanvasElement", HTMLCanvasElement, {
  EM_IMPORT_CONSTRUCTOR HTMLCanvasElement();
  EM_IMPORT_FIELD("width", unsigned long, width);
  EM_IMPORT_FIELD("mozPrintCallback", JSObject, mozPrintCallback);
  EM_IMPORT_FIELD("mozOpaque", bool, mozOpaque);
  EM_IMPORT_FIELD("height", unsigned long, height);
  EM_IMPORT_METHOD("MozGetIPCContext") JSObject MozGetIPCContext(const char* contextId);
  EM_IMPORT_METHOD("captureStream") JSObject captureStream(double frameRate);
  EM_IMPORT_METHOD("mozGetAsFile") JSObject mozGetAsFile(const char* name, JSObject type);
  EM_IMPORT_METHOD("toBlob") void toBlob(JSObject callback, const char* type, JSObject encoderOptions);
  EM_IMPORT_METHOD("getContext") JSObject getContext(const char* contextId, JSObject contextOptions);
  EM_IMPORT_METHOD("transferControlToOffscreen") JSObject transferControlToOffscreen();
  EM_IMPORT_METHOD("toDataURL") const char* toDataURL(const char* type, JSObject encoderOptions);
});
