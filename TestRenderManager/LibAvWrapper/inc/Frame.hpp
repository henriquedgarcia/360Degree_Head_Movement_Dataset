#pragma once

extern "C"
{
   #include <libavutil/imgutils.h>
//   #include <libavutil/parseutils.h>
   #include <libswscale/swscale.h>
}

namespace IMT {
namespace LibAv {

class Frame
{
public:
  Frame(void): m_framePtr(nullptr), m_haveFrame(-1)
  {
    m_framePtr = av_frame_alloc();
  }
  ~Frame(void)
  {
    if (IsValid())
    {
      av_frame_unref(m_framePtr);
      m_haveFrame = -1;
    }
    av_frame_free(&m_framePtr);
    m_framePtr = nullptr;
  }

  bool IsValid(void) const {return m_haveFrame == 0;}
  auto AvCodecReceiveFrame(AVCodecContext* codecCtx) {return m_haveFrame = avcodec_receive_frame(codecCtx, m_framePtr);}
  int64_t GetDisplayTimestamp(void) const {if (IsValid()) {return m_framePtr->pkt_dts;} else {return -1;}}
  int GetWidth(void) const {if (IsValid()) {return m_framePtr->width;} else {return -1;}}
  int GetHeight(void) const {if (IsValid()) {return m_framePtr->height;} else {return -1;}}
  uint8_t** GetDataPtr(void) {if (IsValid()) {return m_framePtr->data;} else {return nullptr;}}
  int* GetRowLength(void) {if (IsValid()) {return m_framePtr->linesize;} else {return nullptr;}}
  size_t GetDisplayPictureNumber(void) const {if (IsValid()) {return m_framePtr->display_picture_number;} else {return -1;}}
private:
  Frame(Frame const&) = delete;
  Frame& operator=(Frame const&) = delete;

  AVFrame* m_framePtr;
  int m_haveFrame;
};

}
}
