#pragma once

#include "em_import.h"

EM_IMPORT_STRUCT("Performance", Performance, {
  EM_IMPORT_FIELD_GETTER("timing", JSObject, timing);
  EM_IMPORT_FIELD("onresourcetimingbufferfull", JSObject, onresourcetimingbufferfull);
  EM_IMPORT_FIELD_GETTER("timeOrigin", double, timeOrigin);
  EM_IMPORT_FIELD_GETTER("navigation", JSObject, navigation);
  EM_IMPORT_FIELD_GETTER("mozMemory", JSObject, mozMemory);
  EM_IMPORT_METHOD("toJSON") JSObject toJSON();
  EM_IMPORT_METHOD("getEntries") JSObject getEntries();
  EM_IMPORT_METHOD("setResourceTimingBufferSize") void setResourceTimingBufferSize(unsigned long maxSize);
  EM_IMPORT_METHOD("clearMeasures") void clearMeasures(const char* measureName);
  EM_IMPORT_METHOD("getEntriesByName") JSObject getEntriesByName(const char* name, const char* entryType);
  EM_IMPORT_METHOD("mark") void mark(const char* markName);
  EM_IMPORT_METHOD("clearMarks") void clearMarks(const char* markName);
  EM_IMPORT_METHOD("getEntriesByType") JSObject getEntriesByType(const char* entryType);
  EM_IMPORT_METHOD("measure") void measure(const char* measureName, const char* startMark, const char* endMark);
  EM_IMPORT_METHOD("clearResourceTimings") void clearResourceTimings();
  EM_IMPORT_METHOD("now") double now();
});
